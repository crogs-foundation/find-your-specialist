"use client";

import { useEffect, useState } from "react";
import styles from "./chat.module.css";
import axios from "axios";
import { useRef } from "react";
import Dropdown from '@/components/Dropdown';
import BackLink from "@/components/BackLink";
import { indexerMap as specialistMap, THINK_REGEX } from "@/constants";




export default function ChatPage() {
    const [prompt, setPrompt] = useState("");
    const [model, setModel] = useState("");
    const [modelList, setModelList] = useState<string[]>([]);
    const [specialist, setSpecialist] = useState("");
    const [specialistList, setSpecialistList] = useState<string[]>([]);
    const [messages, setMessages] = useState<{ role: string; content: string; time: number | undefined }[]>([]);
    const [streamingResponse, setStreamingResponse] = useState("");
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const chatEndRef = useRef<HTMLDivElement | null>(null);
    const textareaRef = useRef<HTMLTextAreaElement | null>(null);

    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = "auto";
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
        }
    }, [prompt]);

    useEffect(() => {
        if (chatEndRef.current) {
            chatEndRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [messages, streamingResponse]);

    useEffect(() => {
        const fetchModels = async () => {
            try {
                const response = await axios.get(`${process.env.API_URL}/models`);
                setModelList(response.data || []);
                if (response.data.length > 0) setModel(response.data[0]); // default to first
            } catch (err) {
                console.error("Failed to fetch models", err);
                setError("Unable to load model list");
            }
        };
        const fetchIndexers = async () => {
            try {
                const response = await axios.get(`${process.env.API_URL}/specialists`);
                setSpecialistList(response.data || []);
                if (response.data.length > 0) setSpecialist(response.data[0]); // default to first
            } catch (err) {
                console.error("Failed to fetch specialists", err);
                setError("Unable to load specialists list");
            }
        };


        fetchIndexers();
        fetchModels();
    }, []);

    const handleSubmit = async () => {
        if (!prompt.trim() || isLoading) return;
        setError("");
        setIsLoading(true);

        // Append user message
        setMessages(prev => [...prev, { role: "user", content: prompt, time: undefined }]);
        setStreamingResponse("");
        setError("");
        const currentPrompt = prompt;
        setPrompt("");
        let current = "";

        try {
            const currentModel = model;
            const response = await fetch(
                `${process.env.API_URL}/chat?prompt=${encodeURIComponent(currentPrompt)}&model=${model}&specialist=${specialist}`,
            );

            if (!response.ok || !response.body) {
                let errorText = undefined;
                try {
                    errorText = (await response.json()).detail;
                }
                catch {

                }

                throw new Error(errorText || "Failed to connect to backend or response body is missing.");
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            let elapsedTime: number | undefined = undefined

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                const messages = chunk.split('\n\n').filter(m => m.trim() !== '');
                for (const message of messages) {
                    try {
                        const parsed = JSON.parse(message);

                        switch (parsed.type) {
                            case 'chunk':
                                current += parsed.data;
                                setStreamingResponse(current);
                                break;
                            case 'complete':
                                setStreamingResponse("");
                                elapsedTime = parsed.data
                                break;
                            case 'error':
                                setError(parsed.data || "Unknown error");
                                setIsLoading(false);
                                return;
                            default:
                                console.warn('Unknown message type:', parsed.type);
                        }
                    } catch (e) {
                        console.error('Error parsing message:', e);
                        setIsLoading(false);
                        return;
                    }
                }
            }
            setStreamingResponse("");
            setMessages(prev => [...prev, { role: currentModel, content: current.replace(THINK_REGEX, '').trim(), time: elapsedTime }]);
        } catch (err) {
            console.error("Error during chat request:", err);
            setError("Error: " + (err instanceof Error ? err.message : "Unknown error"));
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className={styles.page}>
            <h1 className={styles.header}>Chat</h1>

            <div className={styles.controls}>
                <Dropdown
                    options={modelList.map(m => ({ label: m, value: m }))}
                    value={model}
                    onChange={(newValue) => setModel(newValue)}
                />
                <Dropdown
                    options={specialistList.map(value => ({ value: value, label: specialistMap.get(value)! }))}
                    value={specialist}
                    onChange={(newValue) => setSpecialist(newValue)}
                />

            </div>

            <div className={styles.chatBox}>
                {messages.map((msg, idx) => (
                    <div key={idx} className={msg.role === "user" ? styles.userMsg : styles.modelMsg}>
                        <div className={styles.role}><strong>{msg.role === "user" ? "YOU" : msg.role.toUpperCase()}</strong></div>
                        <div>{msg.content}</div>
                        {msg.time && <div className={styles.time}>{msg.time.toFixed(2)} seconds</div>}
                    </div>
                ))}

                {isLoading && (
                    <div className={styles.modelMsg}>
                        <div className={styles.role}><strong>{model.toUpperCase()}</strong></div>
                        <div className={styles.streamingResponse}>{streamingResponse}<span className={styles.spinner}></span></div>

                    </div>
                )}

                {isLoading && (
                    <div className={styles.thinking}>
                        <span>🤖 Thinking...</span>
                    </div>
                )}
                <div ref={chatEndRef} />
            </div>

            <div className={styles.inputRow}>
                <textarea
                    ref={textareaRef}
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === "Enter" && !e.shiftKey) {
                            e.preventDefault();
                            handleSubmit();
                        }
                    }}
                    placeholder="Type your message..."
                    className={styles.textarea}

                />
                <button onClick={handleSubmit} className={styles.sendButton} disabled={isLoading}>
                    Send
                </button>
            </div>

            {error && <div className={styles.error}>{error}</div>}



            <BackLink href="/" />

        </div>
    );
}
