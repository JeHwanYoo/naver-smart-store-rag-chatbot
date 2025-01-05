import {useEffect, useState} from 'react'

export function useStreaming(props: { streamingId: string }) {
  const [streamingContent, setStreamingContent] = useState('')

  useEffect(() => {
    if (!props.streamingId) return

    const eventSource = new EventSource(
      `${import.meta.env.VITE_API_PATH}/v1/streaming/${props.streamingId}`,
    )

    eventSource.onopen = () => {
      setStreamingContent('')
    }

    eventSource.onmessage = (event) => {
      setStreamingContent((prev) => prev + event.data)
    }

    eventSource.onerror = (e) => {
      console.error('SSE connection error.', e)
      eventSource.close()
    }

    return () => {
      eventSource.close()
    }
  }, [props.streamingId])

  return {streamingContent}
}