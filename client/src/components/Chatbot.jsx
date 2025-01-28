import React, { useState } from "react";
import styled from "styled-components";

const Card = styled.div`
  flex: 1;
  min-width: 280px;
  padding: 24px;
  border: 1px solid ${({ theme }) => theme.text_primary + 20};
  border-radius: 14px;
  box-shadow: 1px 6px 20px 0px ${({ theme }) => theme.primary + 15};
  display: flex;
  flex-direction: column;
  gap: 12px;
  background-color: ${({ theme }) => theme.background_secondary};
  @media (max-width: 600px) {
    padding: 16px;
  }
`;

const Title = styled.div`
  font-weight: 600;
  font-size: 18px;
  color: ${({ theme }) => theme.primary};
  @media (max-width: 600px) {
    font-size: 16px;
  }
`;

const ChatWindow = styled.div`
  flex: 1;
  padding: 16px;
  border: 1px solid ${({ theme }) => theme.text_primary + 20};
  border-radius: 10px;
  background-color: ${({ theme }) => theme.background_primary};
  overflow-y: auto;
  max-height: 300px;
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const Message = styled.div`
  font-size: 14px;
  color: ${({ theme }) => theme.text_primary};
  background-color: ${({ user, theme }) =>
    user ? theme.primary + 15 : theme.text_primary + 20};
  padding: 10px;
  border-radius: 8px;
  align-self: ${({ user }) => (user ? "flex-end" : "flex-start")};
  max-width: 75%;
  word-wrap: break-word;
`;

const InputContainer = styled.div`
  display: flex;
  gap: 8px;
  margin-top: 12px;
`;

const Input = styled.input`
  flex: 1;
  padding: 10px;
  border: 1px solid ${({ theme }) => theme.text_primary + 20};
  border-radius: 8px;
  font-size: 14px;
  color: ${({ theme }) => theme.text_primary};
  background-color: ${({ theme }) => theme.background_primary};
`;

const Button = styled.button`
  padding: 10px 16px;
  font-size: 14px;
  font-weight: 600;
  color: ${({ theme }) => theme.background_secondary};
  background-color: ${({ theme }) => theme.primary};
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s ease;
  &:hover {
    background-color: ${({ theme }) => theme.primary_dark};
  }
`;

const ChatBot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (input.trim() === "") return;

    const userMessage = { text: input, user: true };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();
      const botMessage = { text: data.response || "Something went wrong.", user: false };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = { text: "Error: Could not connect to the chatbot backend.", user: false };
      setMessages((prev) => [...prev, errorMessage]);
    }

    setInput("");
  };

  return (
    <Card>
      <Title>Chat Bot</Title>
      <ChatWindow>
        {messages.map((message, index) => (
          <Message key={index} user={message.user}>
            {message.text}
          </Message>
        ))}
      </ChatWindow>
      <InputContainer>
        <Input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message here..."
        />
        <Button onClick={handleSend}>Send</Button>
      </InputContainer>
    </Card>
  );
};

export default ChatBot;
