import { VoiceUpload } from '@/components/VoiceUpload'
import { DocumentUpload } from '@/components/DocumentUpload'
import { ResultsDisplay } from '@/components/ResultsDisplay'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Mic, FileText, Sparkles } from 'lucide-react'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center gap-2 mb-4 px-4 py-2 bg-primary/10 rounded-full">
            <Sparkles className="w-5 h-5 text-primary" />
            <span className="text-sm font-medium text-primary">AI-Powered Voice Processing</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-slate-900 via-slate-700 to-slate-900 dark:from-slate-100 dark:via-slate-300 dark:to-slate-100 bg-clip-text text-transparent">
            Transform Your Audio & Documents
          </h1>
          <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            Upload voice recordings or documents and let our AI extract insights, transcriptions, and actionable intelligence.
          </p>
        </div>

        {/* Main Content */}
        <div className="max-w-4xl mx-auto">
          <Tabs defaultValue="voice" className="w-full">
            <TabsList className="grid w-full grid-cols-2 mb-8">
              <TabsTrigger value="voice" className="gap-2">
                <Mic className="w-4 h-4" />
                Voice Upload
              </TabsTrigger>
              <TabsTrigger value="document" className="gap-2">
                <FileText className="w-4 h-4" />
                Document Upload
              </TabsTrigger>
            </TabsList>

            <TabsContent value="voice" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Upload Voice Recording</CardTitle>
                  <CardDescription>
                    Upload an audio file (MP3, WAV, M4A) and get transcription and analysis
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <VoiceUpload />
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="document" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Upload Document</CardTitle>
                  <CardDescription>
                    Upload a document (PDF, TXT, DOCX) for AI-powered analysis and extraction
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <DocumentUpload />
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>

          {/* Results Section */}
          <div className="mt-12">
            <ResultsDisplay />
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-16 text-center text-sm text-slate-500 dark:text-slate-400">
          <p>Powered by advanced AI • Built with Next.js 14</p>
        </footer>
      </div>
    </main>
  )
}