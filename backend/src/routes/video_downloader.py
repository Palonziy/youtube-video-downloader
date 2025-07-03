from flask import Blueprint, jsonify, request, Response, stream_template
import yt_dlp
import os
import tempfile
import json
from urllib.parse import urlparse
import re
from src.models.user import db
from src.models.download_log import DownloadLog, VideoInfoRequest

video_bp = Blueprint('video', __name__)

def is_valid_youtube_url(url):
    """YouTube URL ni tekshirish"""
    youtube_patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
        r'(?:https?://)?(?:www\.)?youtu\.be/[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/v/[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/shorts/[\w-]+'
    ]
    
    for pattern in youtube_patterns:
        if re.match(pattern, url):
            return True
    return False

def format_duration(duration):
    """Davomiylikni formatlash"""
    if not duration:
        return "Noma_lum"
    
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def format_file_size(size_bytes):
    """Fayl hajmini formatlash"""
    if not size_bytes:
        return "Noma_lum"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

@video_bp.route('/get_video_info', methods=['POST'])
def get_video_info():
    """Video ma'lumotlarini olish"""
    user_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
    user_agent = request.headers.get('User-Agent', '')
    
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            # Xatolikni ma'lumotlar bazasiga yozish
            log_entry = VideoInfoRequest(
                user_ip=user_ip,
                video_url='',
                status='failed',
                error_message='URL talab qilinadi',
                user_agent=user_agent
            )
            db.session.add(log_entry)
            db.session.commit()
            
            return jsonify({'error': 'URL talab qilinadi'}), 400
        
        url = data['url'].strip()
        
        # URL ni tekshirish
        if not is_valid_youtube_url(url):
            # Xatolikni ma'lumotlar bazasiga yozish
            log_entry = VideoInfoRequest(
                user_ip=user_ip,
                video_url=url,
                status='failed',
                error_message='Noto\'g\'ri YouTube URL',
                user_agent=user_agent
            )
            db.session.add(log_entry)
            db.session.commit()
            
            return jsonify({'error': 'Noto\'g\'ri YouTube URL. Faqat YouTube havolalari qo\'llab-quvvatlanadi.'}), 400
        
        # yt-dlp konfiguratsiyasi
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # Video ma'lumotlarini olish
                info = ydl.extract_info(url, download=False)
                
                # Asosiy ma'lumotlar
                video_info = {
                    'title': info.get('title', 'Noma_lum sarlavha'),
                    'duration': format_duration(info.get('duration')),
                    'duration_seconds': info.get('duration'),
                    'thumbnail': info.get('thumbnail'),
                    'uploader': info.get('uploader', 'Noma_lum'),
                    'view_count': info.get('view_count', 0),
                    'upload_date': info.get('upload_date'),
                    'description': info.get('description', '')[:200] + '...' if info.get('description') and len(info.get('description', '')) > 200 else info.get('description', ''),
                }
                
                # Formatlarni olish va filtrlash
                formats = []
                if 'formats' in info:
                    seen_formats = set()
                    for fmt in info['formats']:
                        if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':  # Video va audio bor
                            height = fmt.get('height')
                            ext = fmt.get('ext', 'mp4')
                            filesize = fmt.get('filesize') or fmt.get('filesize_approx')
                            
                            if height and height >= 144:  # Minimal sifat
                                format_key = f"{height}p_{ext}"
                                if format_key not in seen_formats:
                                    seen_formats.add(format_key)
                                    formats.append({
                                        'format_id': fmt.get('format_id'),
                                        'ext': ext,
                                        'height': height,
                                        'quality': f"{height}p",
                                        'filesize': format_file_size(filesize),
                                        'filesize_bytes': filesize,
                                        'fps': fmt.get('fps'),
                                        'vcodec': fmt.get('vcodec'),
                                        'acodec': fmt.get('acodec'),
                                    })
                
                # Formatlarni sifat bo'yicha saralash
                formats.sort(key=lambda x: x['height'], reverse=True)
                
                # Agar formatlar topilmasa, eng yaxshi formatni qo'shish
                if not formats and 'formats' in info:
                    best_format = None
                    for fmt in info['formats']:
                        if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':
                            best_format = fmt
                            break
                    
                    if best_format:
                        height_val = best_format.get('height', 'Noma_lum')
                        quality_text = f"{height_val}p" if height_val != 'Noma_lum' else 'Standart'
                        
                        formats.append({
                            'format_id': best_format.get('format_id'),
                            'ext': best_format.get('ext', 'mp4'),
                            'height': height_val,
                            'quality': quality_text,
                            'filesize': format_file_size(best_format.get('filesize') or best_format.get('filesize_approx')),
                            'filesize_bytes': best_format.get('filesize') or best_format.get('filesize_approx'),
                            'fps': best_format.get('fps'),
                            'vcodec': best_format.get('vcodec'),
                            'acodec': best_format.get('acodec'),
                        })
                
                video_info['formats'] = formats
                
                # Muvaffaqiyatli so'rovni ma'lumotlar bazasiga yozish
                log_entry = VideoInfoRequest(
                    user_ip=user_ip,
                    video_url=url,
                    status='success',
                    user_agent=user_agent
                )
                db.session.add(log_entry)
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'data': video_info
                })
                
            except yt_dlp.DownloadError as e:
                error_msg = str(e)
                
                # Xatolikni ma'lumotlar bazasiga yozish
                log_entry = VideoInfoRequest(
                    user_ip=user_ip,
                    video_url=url,
                    status='error',
                    error_message=error_msg,
                    user_agent=user_agent
                )
                db.session.add(log_entry)
                db.session.commit()
                
                if 'Private video' in error_msg:
                    return jsonify({'error': 'Bu video maxfiy. Maxfiy videolarni yuklab olish mumkin emas.'}), 400
                elif 'Video unavailable' in error_msg:
                    return jsonify({'error': 'Video mavjud emas yoki o\'chirilgan.'}), 400
                elif 'blocked' in error_msg.lower():
                    return jsonify({'error': 'Bu video sizning hududingizda bloklanган.'}), 400
                else:
                    return jsonify({'error': f'Video ma\'lumotlarini olishda xatolik: {error_msg}'}), 400
                    
    except Exception as e:
        # Umumiy xatolikni ma'lumotlar bazasiga yozish
        log_entry = VideoInfoRequest(
            user_ip=user_ip,
            video_url=data.get('url', '') if 'data' in locals() else '',
            status='error',
            error_message=str(e),
            user_agent=user_agent
        )
        db.session.add(log_entry)
        db.session.commit()
        
        return jsonify({'error': f'Serverda xatolik yuz berdi: {str(e)}'}), 500

@video_bp.route('/download_video', methods=['POST'])
def download_video():
    """Videoni yuklab olish"""
    user_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
    user_agent = request.headers.get('User-Agent', '')
    
    try:
        data = request.get_json()
        if not data or 'url' not in data or 'format_id' not in data:
            return jsonify({'error': 'URL va format_id talab qilinadi'}), 400
        
        url = data['url'].strip()
        format_id = data['format_id']
        
        # URL ni tekshirish
        if not is_valid_youtube_url(url):
            return jsonify({'error': 'Noto\'g\'ri YouTube URL'}), 400
        
        # Vaqtinchalik papka yaratish
        temp_dir = tempfile.mkdtemp()
        
        # yt-dlp konfiguratsiyasi
        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # Videoni yuklab olish
                info = ydl.extract_info(url, download=True)
                
                # Yuklab olingan faylni topish
                downloaded_file = None
                for file in os.listdir(temp_dir):
                    if os.path.isfile(os.path.join(temp_dir, file)):
                        downloaded_file = os.path.join(temp_dir, file)
                        break
                
                if not downloaded_file:
                    # Xatolikni ma'lumotlar bazasiga yozish
                    log_entry = DownloadLog(
                        user_ip=user_ip,
                        video_url=url,
                        video_title=info.get('title', 'Noma_lum'),
                        video_uploader=info.get('uploader', 'Noma_lum'),
                        downloaded_format=format_id,
                        status='failed',
                        user_agent=user_agent
                    )
                    db.session.add(log_entry)
                    db.session.commit()
                    
                    return jsonify({'error': 'Fayl yuklab olinmadi'}), 500
                
                # Fayl ma'lumotlarini olish
                file_size = os.path.getsize(downloaded_file)
                file_size_formatted = format_file_size(file_size)
                
                # Muvaffaqiyatli yuklab olishni ma'lumotlar bazasiga yozish
                log_entry = DownloadLog(
                    user_ip=user_ip,
                    video_url=url,
                    video_title=info.get('title', 'Noma_lum'),
                    video_uploader=info.get('uploader', 'Noma_lum'),
                    downloaded_format=format_id,
                    downloaded_quality=data.get('quality', 'Noma_lum'),
                    file_size=file_size_formatted,
                    status='success',
                    user_agent=user_agent
                )
                db.session.add(log_entry)
                db.session.commit()
                
                # Faylni stream qilish
                def generate():
                    try:
                        with open(downloaded_file, 'rb') as f:
                            while True:
                                data = f.read(4096)
                                if not data:
                                    break
                                yield data
                    finally:
                        # Vaqtinchalik fayllarni tozalash
                        try:
                            if os.path.exists(downloaded_file):
                                os.remove(downloaded_file)
                            os.rmdir(temp_dir)
                        except:
                            pass
                
                filename = os.path.basename(downloaded_file)
                
                return Response(
                    generate(),
                    mimetype='application/octet-stream',
                    headers={
                        'Content-Disposition': f'attachment; filename="{filename}"',
                        'Content-Type': 'application/octet-stream'
                    }
                )
                
            except yt_dlp.DownloadError as e:
                # Vaqtinchalik papkani tozalash
                try:
                    os.rmdir(temp_dir)
                except:
                    pass
                
                error_msg = str(e)
                
                # Xatolikni ma'lumotlar bazasiga yozish
                log_entry = DownloadLog(
                    user_ip=user_ip,
                    video_url=url,
                    video_title='Noma_lum',
                    video_uploader='Noma_lum',
                    downloaded_format=format_id,
                    status='error',
                    user_agent=user_agent
                )
                db.session.add(log_entry)
                db.session.commit()
                
                if 'Private video' in error_msg:
                    return jsonify({'error': 'Bu video maxfiy. Maxfiy videolarni yuklab olish mumkin emas.'}), 400
                elif 'Video unavailable' in error_msg:
                    return jsonify({'error': 'Video mavjud emas yoki o\'chirilgan.'}), 400
                else:
                    return jsonify({'error': f'Video yuklab olishda xatolik: {error_msg}'}), 400
                    
    except Exception as e:
        # Umumiy xatolikni ma'lumotlar bazasiga yozish
        log_entry = DownloadLog(
            user_ip=user_ip,
            video_url=data.get('url', '') if 'data' in locals() else '',
            video_title='Noma_lum',
            video_uploader='Noma_lum',
            downloaded_format=data.get('format_id', '') if 'data' in locals() else '',
            status='error',
            user_agent=user_agent
        )
        db.session.add(log_entry)
        db.session.commit()
        
        return jsonify({'error': f'Serverda xatolik yuz berdi: {str(e)}'}), 500

@video_bp.route('/health', methods=['GET'])
def health_check():
    """Server holatini tekshirish"""
    return jsonify({
        'status': 'OK',
        'message': 'YouTube Downloader API ishlayapti'
    })

