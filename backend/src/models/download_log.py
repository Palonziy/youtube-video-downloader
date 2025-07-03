from src.models.user import db
from datetime import datetime

class DownloadLog(db.Model):
    """Foydalanuvchi yuklab olish faoliyatini kuzatish modeli"""
    __tablename__ = 'download_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_ip = db.Column(db.String(45), nullable=False)  # IPv4 va IPv6 uchun
    video_url = db.Column(db.Text, nullable=False)
    video_title = db.Column(db.Text, nullable=True)
    video_uploader = db.Column(db.String(255), nullable=True)
    downloaded_format = db.Column(db.String(50), nullable=False)
    downloaded_quality = db.Column(db.String(20), nullable=True)
    file_size = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='success')  # success, failed, error
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_agent = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<DownloadLog {self.id}: {self.user_ip} - {self.video_title[:50]}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_ip': self.user_ip,
            'video_url': self.video_url,
            'video_title': self.video_title,
            'video_uploader': self.video_uploader,
            'downloaded_format': self.downloaded_format,
            'downloaded_quality': self.downloaded_quality,
            'file_size': self.file_size,
            'status': self.status,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'user_agent': self.user_agent
        }

class VideoInfoRequest(db.Model):
    """Video ma'lumotlari so'rovlarini kuzatish modeli"""
    __tablename__ = 'video_info_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_ip = db.Column(db.String(45), nullable=False)
    video_url = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # success, failed, error
    error_message = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_agent = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<VideoInfoRequest {self.id}: {self.user_ip} - {self.status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_ip': self.user_ip,
            'video_url': self.video_url,
            'status': self.status,
            'error_message': self.error_message,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'user_agent': self.user_agent
        }

