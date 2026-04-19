'use client'

import { useState, useRef } from 'react'
import { Upload, FileText, X, Loader2, CheckCircle2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Progress } from '@/components/ui/progress'
import { cn } from '@/lib/utils'

interface DocumentUploadProps {
  onUploadComplete?: (result: { content: string; entities: string[]; summary: string }) => void
}

export function DocumentUpload({ onUploadComplete }: DocumentUploadProps) {
  const [file, setFile] = useState<File | null>(null)
  const [isDragging, setIsDragging] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploadResult, setUploadResult] = useState<{ content: string; entities: string[]; summary: string } | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const acceptedTypes = [
    'application/pdf',
    'text/plain',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  ]

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile) {
      setFile(droppedFile)
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      setFile(selectedFile)
    }
  }

  const handleUpload = async () => {
    if (!file) return

    setIsUploading(true)
    setUploadProgress(0)

    // Simulate upload progress
    const progressInterval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval)
          return prev
        }
        return prev + 10
      })
    }, 200)

    try {
      // Simulated API call - replace with actual API endpoint
      const formData = new FormData()
      formData.append('file', file)

      // Simulating upload delay
      await new Promise((resolve) => setTimeout(resolve, 2000))

      clearInterval(progressInterval)
      setUploadProgress(100)

      const result = {
        content: 'This is a sample extracted content from the uploaded document. The actual content extraction would be performed by the backend AI service.',
        entities: ['Entity 1', 'Entity 2', 'Entity 3', 'Entity 4'],
        summary: 'Brief summary of the key insights from the document.',
      }

      setUploadResult(result)
      onUploadComplete?.(result)
    } catch (error) {
      console.error('Upload failed:', error)
    } finally {
      setIsUploading(false)
    }
  }

  const clearFile = () => {
    setFile(null)
    setUploadResult(null)
    setUploadProgress(0)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      <div
        className={cn(
          'border-2 border-dashed rounded-lg p-8 text-center transition-colors',
          isDragging
            ? 'border-primary bg-primary/5'
            : 'border-slate-200 dark:border-slate-700 hover:border-primary/50',
          file && 'border-primary/50 bg-primary/5'
        )}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {!file ? (
          <div className="flex flex-col items-center gap-4">
            <div className="p-4 rounded-full bg-slate-100 dark:bg-slate-800">
              <FileText className="w-8 h-8 text-slate-500" />
            </div>
            <div>
              <p className="text-lg font-medium">Drop your document here</p>
              <p className="text-sm text-slate-500">or click to browse</p>
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.txt,.docx"
              onChange={handleFileChange}
              className="hidden"
            />
            <Button onClick={() => fileInputRef.current?.click()} variant="outline">
              <Upload className="w-4 h-4 mr-2" />
              Select File
            </Button>
            <p className="text-xs text-slate-400">Supports PDF, TXT, DOCX (max 10MB)</p>
          </div>
        ) : (
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="p-3 rounded-lg bg-primary/10">
                <FileText className="w-6 h-6 text-primary" />
              </div>
              <div className="text-left">
                <p className="font-medium">{file.name}</p>
                <p className="text-sm text-slate-500">
                  {(file.size / (1024 * 1024)).toFixed(2)} MB
                </p>
              </div>
            </div>
            <Button variant="ghost" size="icon" onClick={clearFile}>
              <X className="w-4 h-4" />
            </Button>
          </div>
        )}
      </div>

      {/* Upload Progress */}
      {isUploading && (
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-slate-500">Analyzing document...</span>
            <span className="font-medium">{uploadProgress}%</span>
          </div>
          <Progress value={uploadProgress} />
        </div>
      )}

      {/* Action Button */}
      {file && !isUploading && (
        <Button onClick={handleUpload} className="w-full" size="lg">
          {isUploading ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Processing...
            </>
          ) : (
            <>
              <FileText className="w-4 h-4 mr-2" />
              Analyze Document
            </>
          )}
        </Button>
      )}

      {/* Result Preview */}
      {uploadResult && (
        <div className="rounded-lg bg-slate-50 dark:bg-slate-800 p-4 space-y-3">
          <div className="flex items-center gap-2 text-green-600">
            <CheckCircle2 className="w-4 h-4" />
            <span className="text-sm font-medium">Document analyzed successfully</span>
          </div>
          <div>
            <Label className="text-xs uppercase text-slate-500">Extracted Entities</Label>
            <div className="flex flex-wrap gap-2 mt-2">
              {uploadResult.entities.map((entity, index) => (
                <span
                  key={index}
                  className="px-2 py-1 text-xs bg-primary/10 text-primary rounded-full"
                >
                  {entity}
                </span>
              ))}
            </div>
          </div>
          <div>
            <Label className="text-xs uppercase text-slate-500">Summary</Label>
            <p className="mt-1 text-sm">{uploadResult.summary}</p>
          </div>
        </div>
      )}
    </div>
  )
}