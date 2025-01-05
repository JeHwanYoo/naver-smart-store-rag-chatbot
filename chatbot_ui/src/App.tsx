import {useState} from 'react'

function mockSendMessage(message: string): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(`챗봇의 응답: "${message}"에 대한 답변입니다.`)
    }, 1000)
  })
}

function App() {
  const [messages, setMessages] = useState<{ sender: string; text: string }[]>([
    {sender: 'bot', text: '안녕하세요! 무엇을 도와드릴까요?'},
  ])
  const [userMessage, setUserMessage] = useState('')

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!userMessage.trim()) return
    const newUserMessage = {sender: 'user', text: userMessage}
    setMessages(prev => [...prev, newUserMessage])
    mockSendMessage(userMessage).then(response => {
      const newBotMessage = {sender: 'bot', text: response}
      setMessages(prev => [...prev, newBotMessage])
    })
    setUserMessage('')
  }

  return (
    <div className="flex h-screen w-full items-center justify-center bg-gray-100">
      <div className="flex h-[90vh] w-full max-w-2xl flex-col rounded-lg bg-white shadow-lg">
        <div className="flex items-center justify-between border-b p-4">
          <h1 className="text-xl font-bold">네이버스마트 스토어 FAQ 챗봇</h1>
        </div>
        <div className="flex-1 overflow-auto p-4">
          {messages.map((msg, idx) => (
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
                {msg.text}
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

export default App