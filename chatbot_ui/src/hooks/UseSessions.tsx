import {useEffect, useState} from 'react'

export function useSessions() {
  const [sessions, setSessions] = useState<{ session_id: string, first_message: string }[]>([])

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_PATH}/v1/sessions/`).then(async r => {
      await r.json().then(setSessions)
    }).catch(console.error)
  }, [])

  return {sessions, setSessions}
}