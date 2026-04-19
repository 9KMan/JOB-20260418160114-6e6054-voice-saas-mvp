'use client'

import { useState } from 'react'
import { Mic, FileText, ChevronDown, ChevronUp, Copy, CheckCheck, Clock, Sparkles } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Progress } from '@/components/ui/progress'
import { cn } from '@/lib/utils'

interface ResultItem {
  id: string
  type: 'voice' | 'document'
  name: string
  date: string
  transcription?: string
  summary?: string
  entities?: string[]
  content?: string
  status: 'completed' | 'processing'
}

export function ResultsDisplay() {
  const [results, setResults] = useState<ResultItem[]>([
    {
      id: '1',
      type: 'voice',
      name: 'meeting_recording.mp3',
      date: '2 hours ago',
      transcription: 'This is a sample transcription from a meeting recording. It contains multiple speakers discussing various topics related to project milestones and deliverables.',
      summary: 'The meeting covered Q4 planning, resource allocation, and upcoming release timelines.',
      status: 'completed',
    },
    {
      id: '2',
      type: 'document',
      name: 'annual_report.pdf',
      date: '1 day ago',
      content: 'Annual report content extracted from the PDF document. Contains financial summaries, performance metrics, and strategic recommendations.',
      entities: ['Revenue', 'Growth', 'Market Share', 'Customers'],
      summary: 'The report shows 25% year-over-year growth with expanded market presence.',
      status: 'completed',
    },
  ])
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set())
  const [copiedId, setCopiedId] = useState<string | null>(null)

  const toggleExpand = (id: string) => {
    const newExpanded = new Set(expandedItems)
    if (newExpanded.has(id)) {
      newExpanded.delete(id)
    } else {
      newExpanded.add(id)
    }
    setExpandedItems(newExpanded)
  }

  const copyToClipboard = async (text: string, id: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedId(id)
      setTimeout(() => setCopiedId(null), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  if (results.length === 0) {
    return (
      <Card>
        <CardContent className="py-12">
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-slate-100 dark:bg-slate-800 mb-4">
              <Sparkles className="w-8 h-8 text-slate-400" />
            </div>
            <h3 className="text-lg font-medium mb-2">No Results Yet</h3>
            <p className="text-sm text-slate-500">
              Upload a voice recording or document to see results here
            </p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Recent Results</h2>
        <span className="text-sm text-slate-500">{results.length} items</span>
      </div>

      <div className="space-y-3">
        {results.map((result) => (
          <Card key={result.id} className="overflow-hidden">
            <div
              className="cursor-pointer"
              onClick={() => toggleExpand(result.id)}
            >
              <CardHeader className="py-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div
                      className={cn(
                        'p-2 rounded-lg',
                        result.type === 'voice'
                          ? 'bg-blue-100 dark:bg-blue-900/30'
                          : 'bg-purple-100 dark:bg-purple-900/30'
                      )}
                    >
                      {result.type === 'voice' ? (
                        <Mic className="w-4 h-4 text-blue-600" />
                      ) : (
                        <FileText className="w-4 h-4 text-purple-600" />
                      )}
                    </div>
                    <div>
                      <CardTitle className="text-base">{result.name}</CardTitle>
                      <CardDescription className="flex items-center gap-2 mt-1">
                        <Clock className="w-3 h-3" />
                        {result.date}
                        {result.status === 'processing' && (
                          <>
                            <span className="mx-1">•</span>
                            <span className="text-blue-600">Processing...</span>
                          </>
                        )}
                      </CardDescription>
                    </div>
                  </div>
                  <Button variant="ghost" size="icon">
                    {expandedItems.has(result.id) ? (
                      <ChevronUp className="w-4 h-4" />
                    ) : (
                      <ChevronDown className="w-4 h-4" />
                    )}
                  </Button>
                </div>
              </CardHeader>

              {result.status === 'processing' && (
                <div className="px-6 pb-2">
                  <Progress value={65} />
                </div>
              )}
            </div>

            {expandedItems.has(result.id) && (
              <CardContent className="pt-0 pb-6">
                <div className="space-y-4">
                  {/* Summary */}
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <Label className="text-xs uppercase text-slate-500">Summary</Label>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="h-6 px-2 text-xs"
                        onClick={(e) => {
                          e.stopPropagation()
                          if (result.summary) copyToClipboard(result.summary, `${result.id}-summary`)
                        }}
                      >
                        {copiedId === `${result.id}-summary` ? (
                          <CheckCheck className="w-3 h-3 mr-1" />
                        ) : (
                          <Copy className="w-3 h-3 mr-1" />
                        )}
                        Copy
                      </Button>
                    </div>
                    <p className="text-sm bg-slate-50 dark:bg-slate-800 rounded-lg p-3">
                      {result.summary || result.content || 'No summary available'}
                    </p>
                  </div>

                  {/* Transcription (for voice) */}
                  {result.type === 'voice' && result.transcription && (
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <Label className="text-xs uppercase text-slate-500">Transcription</Label>
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-6 px-2 text-xs"
                          onClick={(e) => {
                            e.stopPropagation()
                            copyToClipboard(result.transcription!, `${result.id}-transcription`)
                          }}
                        >
                          {copiedId === `${result.id}-transcription` ? (
                            <CheckCheck className="w-3 h-3 mr-1" />
                          ) : (
                            <Copy className="w-3 h-3 mr-1" />
                          )}
                          Copy
                        </Button>
                      </div>
                      <p className="text-sm bg-slate-50 dark:bg-slate-800 rounded-lg p-3">
                        {result.transcription}
                      </p>
                    </div>
                  )}

                  {/* Entities (for documents) */}
                  {result.entities && result.entities.length > 0 && (
                    <div>
                      <Label className="text-xs uppercase text-slate-500 mb-2 block">Extracted Entities</Label>
                      <div className="flex flex-wrap gap-2">
                        {result.entities.map((entity, index) => (
                          <span
                            key={index}
                            className="px-3 py-1 text-xs bg-primary/10 text-primary rounded-full"
                          >
                            {entity}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Actions */}
                  <div className="flex gap-2 pt-2">
                    <Button variant="outline" size="sm">
                      Download Report
                    </Button>
                    <Button variant="outline" size="sm">
                      Share
                    </Button>
                  </div>
                </div>
              </CardContent>
            )}
          </Card>
        ))}
      </div>
    </div>
  )
}