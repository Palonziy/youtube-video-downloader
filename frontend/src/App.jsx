import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import { Download, Play, Clock, Eye, User, FileVideo, Loader2, CheckCircle, AlertCircle, Youtube } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import './App.css'

const API_BASE_URL = 'http://localhost:5001/api'

function App() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [videoInfo, setVideoInfo] = useState(null)
  const [error, setError] = useState('')
  const [downloading, setDownloading] = useState(null)

  const handleGetVideoInfo = async () => {
    if (!url.trim()) {
      setError('YouTube video havolasini kiriting')
      return
    }

    setLoading(true)
    setError('')
    setVideoInfo(null)

    try {
      const response = await fetch(`${API_BASE_URL}/get_video_info`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url.trim() }),
      })

      const data = await response.json()

      if (data.success) {
        setVideoInfo(data.data)
      } else {
        setError(data.error || 'Xatolik yuz berdi')
      }
    } catch (err) {
      setError('Serverga ulanishda xatolik. Iltimos, qaytadan urinib ko\'ring.')
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = async (formatId) => {
    setDownloading(formatId)
    
    try {
      const response = await fetch(`${API_BASE_URL}/download_video`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          url: url.trim(),
          format_id: formatId 
        }),
      })

      if (response.ok) {
        // Faylni yuklab olish
        const blob = await response.blob()
        const downloadUrl = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = downloadUrl
        a.download = `${videoInfo.title}.mp4`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        window.URL.revokeObjectURL(downloadUrl)
      } else {
        const errorData = await response.json()
        setError(errorData.error || 'Yuklab olishda xatolik yuz berdi')
      }
    } catch (err) {
      setError('Yuklab olishda xatolik yuz berdi')
    } finally {
      setDownloading(null)
    }
  }

  const formatViewCount = (count) => {
    if (count >= 1000000000) {
      return (count / 1000000000).toFixed(1) + 'B'
    } else if (count >= 1000000) {
      return (count / 1000000).toFixed(1) + 'M'
    } else if (count >= 1000) {
      return (count / 1000).toFixed(1) + 'K'
    }
    return count?.toString() || '0'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-red-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-red-100 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-center space-x-3">
            <div className="p-2 bg-red-500 rounded-xl">
              <Youtube className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">YouTube Downloader</h1>
              <p className="text-sm text-gray-600">Bepul video yuklab olish xizmati</p>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {/* URL Input Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Card className="mb-8 shadow-lg border-red-100">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl text-gray-900">Video Havolasini Kiriting</CardTitle>
              <CardDescription className="text-gray-600">
                YouTube video havolasini quyidagi maydonга joylashtiring
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex space-x-2">
                <Input
                  type="url"
                  placeholder="https://www.youtube.com/watch?v=..."
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  className="flex-1 h-12 text-lg border-red-200 focus:border-red-400"
                  onKeyPress={(e) => e.key === 'Enter' && handleGetVideoInfo()}
                />
                <Button 
                  onClick={handleGetVideoInfo}
                  disabled={loading}
                  className="h-12 px-8 bg-red-500 hover:bg-red-600 text-white"
                >
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Yuklanmoqda...
                    </>
                  ) : (
                    <>
                      <Play className="mr-2 h-4 w-4" />
                      Tahlil qilish
                    </>
                  )}
                </Button>
              </div>

              {/* Error Message */}
              <AnimatePresence>
                {error && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="flex items-center space-x-2 p-3 bg-red-50 border border-red-200 rounded-lg"
                  >
                    <AlertCircle className="h-5 w-5 text-red-500" />
                    <span className="text-red-700">{error}</span>
                  </motion.div>
                )}
              </AnimatePresence>
            </CardContent>
          </Card>
        </motion.div>

        {/* Video Info Section */}
        <AnimatePresence>
          {videoInfo && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              <Card className="mb-8 shadow-lg border-red-100">
                <CardContent className="p-6">
                  <div className="grid md:grid-cols-3 gap-6">
                    {/* Video Thumbnail */}
                    <div className="md:col-span-1">
                      <div className="relative rounded-lg overflow-hidden shadow-md">
                        <img 
                          src={videoInfo.thumbnail} 
                          alt={videoInfo.title}
                          className="w-full h-auto object-cover"
                        />
                        <div className="absolute inset-0 bg-black/20 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
                          <Play className="h-12 w-12 text-white" />
                        </div>
                      </div>
                    </div>

                    {/* Video Details */}
                    <div className="md:col-span-2 space-y-4">
                      <div>
                        <h2 className="text-xl font-bold text-gray-900 mb-2">{videoInfo.title}</h2>
                        <div className="flex flex-wrap gap-2 mb-3">
                          <Badge variant="secondary" className="flex items-center space-x-1">
                            <User className="h-3 w-3" />
                            <span>{videoInfo.uploader}</span>
                          </Badge>
                          <Badge variant="secondary" className="flex items-center space-x-1">
                            <Eye className="h-3 w-3" />
                            <span>{formatViewCount(videoInfo.view_count)} ko'rishlar</span>
                          </Badge>
                          <Badge variant="secondary" className="flex items-center space-x-1">
                            <Clock className="h-3 w-3" />
                            <span>{videoInfo.duration}</span>
                          </Badge>
                        </div>
                        {videoInfo.description && (
                          <p className="text-gray-600 text-sm leading-relaxed">
                            {videoInfo.description}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Download Options */}
              <Card className="shadow-lg border-red-100">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Download className="h-5 w-5 text-red-500" />
                    <span>Yuklab Olish Variantlari</span>
                  </CardTitle>
                  <CardDescription>
                    Kerakli sifat va formatni tanlang
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {videoInfo.formats.map((format, index) => (
                      <motion.div
                        key={format.format_id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200 hover:border-red-200 transition-colors"
                      >
                        <div className="flex items-center space-x-4">
                          <div className="p-2 bg-red-100 rounded-lg">
                            <FileVideo className="h-5 w-5 text-red-600" />
                          </div>
                          <div>
                            <div className="flex items-center space-x-2">
                              <span className="font-semibold text-gray-900">{format.quality}</span>
                              <Badge variant="outline">{format.ext.toUpperCase()}</Badge>
                            </div>
                            <div className="text-sm text-gray-600">
                              Hajmi: {format.filesize} • FPS: {format.fps || 'N/A'}
                            </div>
                          </div>
                        </div>
                        <Button
                          onClick={() => handleDownload(format.format_id)}
                          disabled={downloading === format.format_id}
                          className="bg-red-500 hover:bg-red-600 text-white"
                        >
                          {downloading === format.format_id ? (
                            <>
                              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                              Yuklanmoqda...
                            </>
                          ) : (
                            <>
                              <Download className="mr-2 h-4 w-4" />
                              Yuklab olish
                            </>
                          )}
                        </Button>
                      </motion.div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Features Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mt-12"
        >
          <Card className="shadow-lg border-red-100">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl text-gray-900">Nima uchun bizni tanlash kerak?</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-3 gap-6">
                <div className="text-center space-y-3">
                  <div className="p-3 bg-red-100 rounded-full w-fit mx-auto">
                    <CheckCircle className="h-8 w-8 text-red-600" />
                  </div>
                  <h3 className="font-semibold text-gray-900">Bepul va Tez</h3>
                  <p className="text-sm text-gray-600">
                    Hech qanday to'lov talab qilinmaydi. Videolarni tez va oson yuklab oling.
                  </p>
                </div>
                <div className="text-center space-y-3">
                  <div className="p-3 bg-red-100 rounded-full w-fit mx-auto">
                    <FileVideo className="h-8 w-8 text-red-600" />
                  </div>
                  <h3 className="font-semibold text-gray-900">Yuqori Sifat</h3>
                  <p className="text-sm text-gray-600">
                    Turli sifat va formatlarni qo'llab-quvvatlaydi. HD dan 4K gacha.
                  </p>
                </div>
                <div className="text-center space-y-3">
                  <div className="p-3 bg-red-100 rounded-full w-fit mx-auto">
                    <Download className="h-8 w-8 text-red-600" />
                  </div>
                  <h3 className="font-semibold text-gray-900">Oson Foydalanish</h3>
                  <p className="text-sm text-gray-600">
                    Faqat havolani joylashtiring va yuklab olish tugmasini bosing.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 mt-16">
        <div className="container mx-auto px-4 text-center">
          <div className="flex items-center justify-center space-x-3 mb-4">
            <div className="p-2 bg-red-500 rounded-xl">
              <Youtube className="h-6 w-6 text-white" />
            </div>
            <span className="text-xl font-bold">YouTube Downloader</span>
          </div>
          <p className="text-gray-400 text-sm">
            © 2024 YouTube Downloader. Barcha huquqlar himoyalangan.
          </p>
          <p className="text-gray-500 text-xs mt-2">
            Faqat shaxsiy foydalanish uchun. Mualliflik huquqlarini hurmat qiling.
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App

