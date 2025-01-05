import React, {useEffect, useState} from 'react'
import {v4 as uuidv4} from 'uuid'
import {useStreaming} from './hooks/UseStreaming'
import {useSessions} from './hooks/UseSessions'
import DOMPurify from 'dompurify'
import {useMessagesBySession} from './hooks/UseMessagesBySession.tsx'

function generateUUID() {
  return uuidv4()
}

export default function App() {
  const {sessions, setSessions} = useSessions()
  const [currentSessionId, setCurrentSessionId] = useState<string>('')
  const [userMessage, setUserMessage] = useState('')
  const [streamingId, setStreamingId] = useState('')

  const {messagesBySession, setMessagesBySession} = useMessagesBySession({sessionId: currentSessionId})
  const {streamingContent} = useStreaming({streamingId})

  // 처음 마운트될 때 자동으로 새 대화를 생성
  useEffect(() => {
    handleNewConversation()
  }, [])

  // streaming 값이 변경될 때마다 마지막 봇 메시지로 실시간 반영
  useEffect(() => {
    if (!streamingContent) return
    if (!currentSessionId) return

    setMessagesBySession((prev) => {
      const currentMessages = prev[currentSessionId] || []
      // 마지막 메시지가 봇(bot)인지 확인
      const lastMessage = currentMessages[currentMessages.length - 1]

      // 만약 마지막 메시지가 'bot'이 아니라면 새 메시지를 추가
      if (!lastMessage || lastMessage.sender !== 'bot') {
        return {
          ...prev,
          [currentSessionId]: [
            ...currentMessages,
            {sender: 'bot', text: streamingContent},
          ],
        }
      } else {
        // 마지막 메시지가 'bot'이면 해당 메시지에 문자열을 갱신
        const updatedLastMessage = {
          ...lastMessage,
          text: streamingContent,
        }
        return {
          ...prev,
          [currentSessionId]: [
            ...currentMessages.slice(0, -1),
            updatedLastMessage,
          ],
        }
      }
    })
  }, [streamingContent, currentSessionId])

  function handleNewConversation() {
    const newSessionId = generateUUID()
    setCurrentSessionId(newSessionId)
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!userMessage.trim() || !currentSessionId) return

    const newUserMessage = {sender: 'user', text: userMessage}
    setMessagesBySession((prev) => {
      const currentMessages = prev[currentSessionId] || []
      return {
        ...prev,
        [currentSessionId]: [...currentMessages, newUserMessage],
      }
    })

    const foundSession = sessions.find((s) => s.session_id === currentSessionId)
    if (!foundSession) {
      setSessions((prev) => [
        {
          session_id: currentSessionId,
          first_message: userMessage,
        },
        ...prev,
      ])
    }

    // 서버에 user_message 전송 후, streamingId 수신
    const postResult = await fetch(
      `${import.meta.env.VITE_API_PATH}/v1/sessions/${currentSessionId}/chats`,
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json; charset=utf-8'},
        body: JSON.stringify({user_message: userMessage}),
      },
    )
    const {streaming_id} = await postResult.json()
    setStreamingId(streaming_id)

    setUserMessage('')
  }

  return (
    <div className="flex h-screen w-full bg-gray-100">
      <div className="w-1/4 border-r bg-white p-4">
        <button
          className="w-full bg-green-500 text-white p-2 rounded mb-4"
          onClick={handleNewConversation}
        >
          새로운 대화
        </button>
        {sessions.map((session) => (
          <div
            key={session.session_id}
            onClick={() => setCurrentSessionId(session.session_id)}
            className={`cursor-pointer rounded p-2 mb-2 max-w-full overflow-hidden text-ellipsis whitespace-nowrap ${
              currentSessionId === session.session_id
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 text-gray-800'
            }`}
          >
            {session.first_message}
          </div>
        ))}
      </div>

      <div className="flex flex-col w-3/4 h-[90vh] max-w-2xl mx-auto my-auto rounded-lg bg-white shadow-lg">
        <div className="flex items-center justify-between border-b p-4">
          <h1 className="text-xl font-bold">네이버스마트 스토어 FAQ 챗봇</h1>
        </div>

        <div className="flex-1 overflow-auto p-4">
          {(messagesBySession[currentSessionId] || []).map((msg, idx) => (
            <div
              key={idx}
              className={`mb-2 flex ${
                msg.sender === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`rounded-md px-3 py-2 text-sm ${
                  msg.sender === 'user'
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-800'
                }`}
              >
                {msg.sender === 'bot' && <>🤖 챗봇<br/></>}
                {msg.sender === 'bot' ?
                  <div dangerouslySetInnerHTML={{__html: DOMPurify.sanitize(msg.text)}}></div> : msg.text}
              </div>
            </div>
          ))}
        </div>

        <form onSubmit={handleSubmit} className="border-t p-4">
          <div className="flex gap-2">
            <input
              type="text"
              value={userMessage}
              onChange={(e) => setUserMessage(e.target.value)}
              className="flex-1 rounded border border-gray-300 p-2 outline-none focus:border-blue-400"
              placeholder="메시지를 입력하세요..."
            />
            <button
              type="submit"
              className="rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
            >
              전송
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}