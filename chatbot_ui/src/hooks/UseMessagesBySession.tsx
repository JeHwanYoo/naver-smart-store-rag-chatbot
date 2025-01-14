import {useEffect, useState} from 'react'

export function useMessagesBySession(props: { sessionId: string }) {
  const [messagesBySession, setMessagesBySession] = useState<{
    [session_id: string]: { sender: string; text: string }[]
  }>({})

  useEffect(() => {
    if (!props.sessionId) return
    if (!messagesBySession[props.sessionId]) {
      fetch(`${import.meta.env.VITE_API_PATH}/v1/sessions/${props.sessionId}/chats`).then(async r => {
        const chats = await r.json()

        for (const chat of chats) {
          setMessagesBySession((prev) => ({
            ...prev,
            [props.sessionId]: [
              ...(prev[props.sessionId] ?? []),
              {sender: 'user', text: chat.user_message},
              {sender: 'bot', text: chat.system_message},
            ],
          }))
        }
      }).catch(console.error)
    }
  }, [props.sessionId])

  return {messagesBySession, setMessagesBySession}
}