import axios from "axios";
import { Conversation } from "../datatype";

export const CHAT_API = {
    ask: (conversation: Conversation[], model: string) => {
        return axios.post(process.env.NEXT_PUBLIC_SERVER_API + `/ask?model=${model}`, 
            {conversation_history: conversation}, 
            {
                headers: 
                    {'Content-Type': 'application/json'},
                responseType: 'stream'
            })
    },
    update_token: (conversation: Conversation[], response_chat: string, model: string) => {
        return axios.put(process.env.NEXT_PUBLIC_SERVER_API + `/update_token?model=${model}`, {
            req: {conversation_history: conversation},
            res: {response: response_chat}
        })
    },
    get_token: () => {
        return axios.get(process.env.NEXT_PUBLIC_SERVER_API + '/token')
    }
}
