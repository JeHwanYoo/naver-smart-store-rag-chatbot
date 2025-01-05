import React, {useEffect, useState, useRef} from 'react'
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
  const {streamingContent, isStreaming} = useStreaming({streamingId})

  // 메시지 컨테이너의 끝을 참조할 ref 생성
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // 스크롤을 맨 아래로 내리는 함수
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({behavior: 'smooth'})
  }

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
      const lastMessage = currentMessages[currentMessages.length - 1]

      if (!lastMessage || lastMessage.sender !== 'bot') {
        return {
          ...prev,
          [currentSessionId]: [
            ...currentMessages,
            {sender: 'bot', text: streamingContent},
          ],
        }
      } else {
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

    // 메시지가 업데이트 된 후 스크롤을 맨 아래로 내림
    scrollToBottom()
  }, [streamingContent, currentSessionId])

  // 메시지가 변경될 때마다 스크롤을 맨 아래로 내림
  useEffect(() => {
    scrollToBottom()
  }, [messagesBySession, currentSessionId])

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
          className={`
            w-full p-2 rounded mb-4
            text-white bg-green-500
            hover:bg-green-600
            disabled:bg-gray-400 disabled:cursor-not-allowed
          `}
          onClick={handleNewConversation}
          disabled={isStreaming}
        >
          새로운 대화
        </button>

        {sessions.map((session) => {
          const isCurrent = currentSessionId === session.session_id
          return (
            <button
              key={session.session_id}
              onClick={() => setCurrentSessionId(session.session_id)}
              disabled={isStreaming}
              className={`
                cursor-pointer rounded p-2 mb-2 max-w-full
                overflow-hidden text-ellipsis whitespace-nowrap
                ${isCurrent ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'}
                disabled:bg-gray-400 disabled:text-gray-200
                disabled:cursor-not-allowed
              `}
            >
              {session.first_message}
            </button>
          )
        })}
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
                {msg.sender === 'bot' && (
                  <>
                    🤖 챗봇<br/>
                  </>
                )}
                {msg.sender === 'bot' ? (
                  <div
                    dangerouslySetInnerHTML={{
                      __html: DOMPurify.sanitize(msg.text),
                    }}
                  ></div>
                ) : (
                  msg.text
                )}
              </div>
            </div>
          ))}
          {/* 스크롤을 내리기 위한 빈 div */}
          <div ref={messagesEndRef}/>
        </div>

        <form
          onSubmit={isStreaming ? (e) => e.preventDefault() : handleSubmit}
          className="border-t p-4"
        >
          <div className="flex gap-2">
            <input
              type="text"
              value={userMessage}
              onChange={(e) => setUserMessage(e.target.value)}
              disabled={isStreaming}
              className="flex-1 rounded border border-gray-300 p-2 outline-none focus:border-blue-400"
              placeholder="메시지를 입력하세요..."
            />
            <button
              type="submit"
              disabled={isStreaming}
              className="rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              전송
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}