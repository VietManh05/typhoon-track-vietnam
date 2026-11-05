import React, { FormEvent, useState } from "react";
import { Bot, Send, ShieldAlert, Sparkles } from "lucide-react";
import { Language } from "../i18n";
import { askOllama, OllamaChatMessage } from "../services/api";
import ReactMarkdown from "react-markdown";

const MAX_QUESTION_LENGTH = 2000;

export const OllamaAssistant: React.FC<{ lang: Language }> = ({ lang }) => {
    const vi = lang === "vi";
    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState<OllamaChatMessage[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const suggestions = vi
        ? ["Giải thích nón bất định", "Cần làm gì khi có cảnh báo bão?", "Phân biệt áp thấp và bão"]
        : ["Explain the uncertainty cone", "What should I do during a typhoon warning?", "Tropical depression vs typhoon"];

    const submit = async (event: FormEvent) => {
        event.preventDefault();
        const content = question.trim();
        if (!content || loading) return;

        setQuestion("");
        setError(null);
        setLoading(true);
        const history = messages.slice(-6);
        setMessages((current) => [...current, { role: "user", content }]);
        try {
            const response = await askOllama(content, history, lang);
            setMessages((current) => [
                ...current,
                { role: "assistant", content: response.answer },
            ]);
        } catch (cause) {
            setError(
                cause instanceof Error
                    ? cause.message
                    : vi
                      ? "Trợ lý AI tạm thời không khả dụng."
                      : "AI assistant is temporarily unavailable.",
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <section className="ai-assistant" aria-labelledby="ai-assistant-title">
            <div className="ai-assistant-head">
                <span className="ai-assistant-mark" aria-hidden="true"><Sparkles /></span>
                <div>
                    <span className="eyebrow">OLLAMA CLOUD</span>
                    <h2 id="ai-assistant-title">{vi ? "Trợ lý khí tượng AI" : "AI weather assistant"}</h2>
                    <p>{vi ? "Giải thích thuật ngữ và hướng dẫn an toàn" : "Weather explanations and safety guidance"}</p>
                </div>
            </div>

            <div className="ai-safety-note" role="note">
                <ShieldAlert aria-hidden="true" />
                <span>
                    <span className="hidden sm:inline">{vi ? "AI có thể sai. Không dùng thay bản tin NCHMF hoặc chỉ đạo của cơ quan chức năng." : "AI can be wrong. Do not replace NCHMF bulletins or local authority guidance."}</span>
                    <span className="sm:hidden">{vi ? "AI có thể sai. Đối chiếu bản tin chính thức." : "AI can be wrong. Check official bulletins."}</span>
                </span>
                <a href="https://nchmf.gov.vn/kttvsite/" target="_blank" rel="noopener noreferrer">
                    <span className="hidden sm:inline">{vi ? "Xem bản tin NCHMF" : "NCHMF bulletins"}</span>
                    <span className="sm:hidden">NCHMF ↗</span>
                </a>
            </div>

            <div className="ai-messages" aria-live="polite" aria-busy={loading}>
                {messages.length === 0 ? (
                    <div className="ai-welcome">
                        <Bot aria-hidden="true" />
                        <p>{vi ? "Bạn muốn tìm hiểu điều gì về thời tiết và bão?" : "What would you like to learn about weather and typhoons?"}</p>
                        <div className="ai-suggestions">
                            {suggestions.map((item) => (
                                <button key={item} type="button" onClick={() => setQuestion(item)}>{item}</button>
                            ))}
                        </div>
                    </div>
                ) : (
                    <ol>
                        {messages.map((message, index) => (
                            <li key={`${message.role}-${index}`} className={`ai-message ${message.role}`}>
                                <span>{message.role === "user" ? (vi ? "Bạn" : "You") : "Ollama"}</span>
                                {message.role === "assistant" ? (
                                    <div className="ai-message-body">
                                        <ReactMarkdown skipHtml components={{ img: ({ alt }) => <span>{alt}</span> }}>
                                            {message.content}
                                        </ReactMarkdown>
                                    </div>
                                ) : <p>{message.content}</p>}
                            </li>
                        ))}
                    </ol>
                )}
                {loading && <p className="ai-thinking" role="status">{vi ? "Ollama đang suy nghĩ…" : "Ollama is thinking…"}</p>}
            </div>

            {error && <p className="ai-error" role="alert">{error}</p>}

            <form className="ai-composer" onSubmit={submit}>
                <label htmlFor="ai-question" className="sr-only">{vi ? "Câu hỏi cho trợ lý AI" : "Question for AI assistant"}</label>
                <textarea
                    id="ai-question"
                    value={question}
                    maxLength={MAX_QUESTION_LENGTH}
                    rows={3}
                    onChange={(event) => setQuestion(event.target.value)}
                    onKeyDown={(event) => {
                        if (event.key === "Enter" && !event.shiftKey) {
                            event.preventDefault();
                            event.currentTarget.form?.requestSubmit();
                        }
                    }}
                    placeholder={vi ? "Hỏi về thời tiết, bão hoặc cách ứng phó…" : "Ask about weather, typhoons, or preparedness…"}
                    aria-describedby="ai-question-help"
                />
                <div>
                    <span id="ai-question-help">{vi ? "Enter để gửi · Shift+Enter xuống dòng" : "Enter to send · Shift+Enter for a new line"}</span>
                    <button type="submit" disabled={!question.trim() || loading} aria-label={vi ? "Gửi câu hỏi" : "Send question"}>
                        <Send aria-hidden="true" />
                    </button>
                </div>
            </form>
        </section>
    );
};
