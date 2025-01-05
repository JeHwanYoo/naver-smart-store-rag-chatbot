import {useState} from 'react'
import {useSessions} from './hooks/UseSessions.tsx'

function generateTempSessionId() {
  return 'temp_' + Date.now()
}

export default function App() {
  const {sessions, setSessions} = useSessions()

  const [currentSessionId, setCurrentSessionId] = useState<string>('dummy_uuid_1')
  const [messagesBySession, setMessagesBySession] = useState<{
    [session_id: string]: { sender: string; text: string }[]
  }>({
    dummy_uuid_1: [{sender: 'bot', text: '안녕하세요! 무엇을 도와드릴까요?'}],
    dummy_uuid_2: [{sender: 'bot', text: '안녕하세요! 무엇을 도와드릴까요?'}],
    dummy_uuid_3: [{sender: 'bot', text: '안녕하세요! 무엇을 도와드릴까요?'}],
  })

  const [userMessage, setUserMessage] = useState('')

  function mockSendMessage(message: string): Promise<string> {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(`"${message}"에 대한 답변입니다: `)
      }, 1000)
    })
  }

  function handleNewConversation() {
    const newTempId = generateTempSessionId()
    setCurrentSessionId(newTempId)
    setMessagesBySession((prev) => ({
      ...prev,
      [newTempId]: [{sender: 'bot', text: '안녕하세요! 무엇을 도와드릴까요?'}],
    }))
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!userMessage.trim()) return
    if (!currentSessionId) return

    const newUserMessage = {sender: 'user', text: userMessage}

    setMessagesBySession((prev) => {
      const currentMessages = prev[currentSessionId] || []
      return {
        ...prev,
        [currentSessionId]: [...currentMessages, newUserMessage],
      }
    })

    const foundSession = sessions.find(
      (s) => s.session_id === currentSessionId,
    )
    if (!foundSession) {
      setSessions((prev) => [
        {
          session_id: currentSessionId,
          first_message: userMessage,
        },
        ...prev,
      ])
    }

    mockSendMessage(userMessage).then((response) => {
      const newBotMessage = {sender: 'bot', text: response}
      setMessagesBySession((prev) => {
        const currentMessages = prev[currentSessionId] || []
        return {
          ...prev,
          [currentSessionId]: [...currentMessages, newBotMessage],
        }
      })
    })
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

        {currentSessionId ? (
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
                  {msg.text}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="flex-1 overflow-auto p-4 flex items-center justify-center text-gray-500">
            새로운 세션이 선택되었습니다.
            <br/>
            아직 대화가 없습니다.
          </div>
        )}

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