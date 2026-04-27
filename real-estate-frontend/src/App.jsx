import "./styles/index.css";
import { useChat } from "./hooks/useChat.jsx";
import { useDarkMode } from "./hooks/useDarkMode.jsx";
import Header from "./components/Header.jsx";
import ExampleQuestions from "./components/ExampleQuestions.jsx";
import ChatBox from "./components/ChatBox.jsx";
import InputArea from "./components/InputArea.jsx";
import RagasResult from "./components/RagasResult.jsx";

export default function App() {
  const { messages, loading, sendMessage, resetChat } = useChat();
  const { isDark, toggleDark } = useDarkMode();

  return (
    <div className="page">
      <Header onReset={resetChat} isDark={isDark} onToggleDark={toggleDark} />
      <main className="main">
        <ExampleQuestions onSelect={sendMessage} disabled={loading} />
        <div className="chat-container">
          <ChatBox messages={messages} loading={loading} />
          <InputArea onSend={sendMessage} loading={loading} />
        </div>
        <div className="chat-container" style={{ padding: "0 18px" }}>
          <RagasResult />
        </div>
      </main>
    </div>
  );
}