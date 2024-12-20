"use client"
import Image from "next/image";
import { useState, useEffect, useRef } from "react";
import { Input, Button, Card } from "antd";
import ReactMarkdown from "react-markdown";
import { Conversation } from "../datatype";
import { CHAT_API } from "../api";

const { TextArea } = Input

export default function Home() {
    const [logo, setLogo] = useState(true);
    const [message, setMessage] = useState<string>("")
    const [conversationHistory, setConversationHistory] = useState<Conversation[]>([])
    const [model, setModel] = useState<string>('')
    const [token, setToken] = useState<number>(0)
    const [finishReason, setFinishReason] = useState<boolean>(true)
    const containerRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        if (containerRef.current) {
        containerRef.current.scrollTop = containerRef.current.scrollHeight;
        }
    }, [conversationHistory])

    useEffect(() => {
        const get_status = async () => {
            const fetch_status = await CHAT_API.get_token()
            setModel(fetch_status.data.model_name)
            setToken(fetch_status.data.token_remaining)
        }

        get_status()
    }, [])
    
    const updateLatestResponse = (chunk: string) => {
        setConversationHistory((prev) => {
            const prev_conversation: Conversation[] = [...prev]
            const lastIndex = prev_conversation.length - 1
            prev_conversation[lastIndex] = {
                role: prev_conversation[lastIndex].role, 
                message: [...prev_conversation[lastIndex].message, [chunk]]
            }

            return prev_conversation
        })
    }

    const stopAndStartNewResponse = () => {
        setConversationHistory(prev => [...prev, {role: 'assistant', message: []}])
    }

    const handleEnter= async () => {
        const msg_saved = message
        const current_conversation: Conversation[] = [...conversationHistory, {role: 'user', message: [[msg_saved]]}]
        // Save user message
        setConversationHistory(current_conversation)
        setMessage("")


        const fetch_response = await fetch(process.env.NEXT_PUBLIC_SERVER_API + `/ask?model=${model}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                conversation_history: current_conversation
            })
        })

        const reader = fetch_response.body?.getReader()
        const decoder = new TextDecoder()
        let done = false

        if (reader) {
            stopAndStartNewResponse()
            let res_answer: string = ''
            while (!done) {
                const {value, done: readerDone} = await reader.read()
                done = readerDone

                if (value) {
                    const chunk = decoder.decode(value, {stream: true})
                    updateLatestResponse(chunk)
                    res_answer += chunk
                }
            }
            console.log(res_answer)
            const update = await CHAT_API.update_token(current_conversation, res_answer, model)
            setModel(update.data.model_name)
            setToken(update.data.token_remaining)
        }
    }

    useEffect(() => {
         const LogoCounter = () => {
            setTimeout(() => {
                setLogo(false);
            }, 4000);
        }
        LogoCounter();
    })

    return (
        <div className="items-center justify-items-center min-h-screen font-[family-name:var(--font-geist-sans)]">
            <main className="flex flex-col items-center w-screen h-screen">
                {logo && <Image
                        className="dark:invert animate-fadeInOut"
                        src="/next.svg"
                        alt="Next.js logo"
                        width={180}
                        height={38}
                        priority
                    />
                }

                {!logo && <>
                    {/* Chat Box */}
                    <div className="w-full h-[90%] border-2 overflow-y-auto gap-5 shadow-md flex flex-col item-end" id="chat-container" ref={containerRef}>
                        {conversationHistory.map((msg, index) => {
                            // if (index < response.length - 1)
                                return (
                                <div key={index} className={`flex w-full ${msg.role == 'user' ? 'justify-end' : 'justify-start'}`}>
                                    <Card className="px-4 py-2 rounded-lg w-fit max-w-[80%] m-4">
                                        <ReactMarkdown>{msg.message.flat().join("")}</ReactMarkdown>
                                    </Card>
                                </div>
                                )
                        })}
                    </div>
                    {/* Chat Area */}
                    <div className="w-full h-[5%]">
                        <TextArea
                            className="overflow-auto w-full h-full"
                            placeholder="Type your message here"    
                            autoSize={{minRows: 1, maxRows: 6}}
                            value={message}
                            onChange={e => setMessage(e.target.value)}
                            onPressEnter={handleEnter}
                        />
                        <div>Using: {model} - Token Remaining: {token}</div>
                    </div>
                </>}
            </main>
        </div>
    );
}
