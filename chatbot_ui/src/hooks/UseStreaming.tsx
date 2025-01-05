import {useEffect, useState} from 'react'

export function useStreaming(props: { streamingId: string }) {
  const [streamingContent, setStreamingContent] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)

  useEffect(() => {
    if (!props.streamingId) return

    const eventSource = new EventSource(
      `${import.meta.env.VITE_API_PATH}/v1/streaming/${props.streamingId}`,
    )

    eventSource.onopen = () => {
      setIsStreaming(true)
      setStreamingContent('')
    }

    eventSource.onmessage = (event) => {
      setStreamingContent((prev) => prev + event.data)
    }

    eventSource.onerror = () => {
      setIsStreaming(false)
      eventSource.close()
    }

    return () => {
      setIsStreaming(false)
      eventSource.close()
    }
  }, [props.streamingId])

  return {streamingContent, isStreaming}
}