import { useState } from "react";
import { API_URL } from "../constants/index.jsx";

const STREAM_URL = "http://localhost:8000/chat/stream";

const INITIAL_MESSAGE = {
  role: "bot",
  content: "안녕하세요! 부동산 법률 챗봇입니다. 부동산 관련 법률에 관한 궁금한 점을 자유롭게 질문해 주세요.",
};

export function useChat() {
  const [messages, setMessages] = useState([INITIAL_MESSAGE]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (question) => {
    if (!question.trim() || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setLoading(true);

    try {
      const res = await fetch(STREAM_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      // 답변 한글자씩 출력 시키기
      //reader      → 서버에서 데이터를 조금씩 읽어오는 것
      // decoder     → 받아온 데이터를 텍스트로 변환
      // while(true) → 데이터가 끝날 때까지 계속 읽기
      // chunk       → 조금씩 받아온 텍스트 조각
      // content + chunk → 기존 텍스트에 조각을 계속 붙여나가기
      const reader = res.body.getReader();
      const decoder = new TextDecoder();

      setMessages((prev) => [...prev, { role: "bot", content: "" }]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            role: "bot",
            content: updated[updated.length - 1].content + chunk,
          };
          return updated;
        });
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: "서버 연결에 실패했습니다. 서버가 실행 중인지 확인해 주세요.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const resetChat = () => {
    setMessages([INITIAL_MESSAGE]);
  };

  return { messages, loading, sendMessage, resetChat };
}