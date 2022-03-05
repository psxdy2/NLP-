import botAvatar from '../assets/sara_avatar.png'
import userAvatar from '../assets/userAvatar.jpg'
import {defaultQuickReplies} from "./quickReplys";
import {createTextBotMsg} from "../utils/msgManager";


const initialMessages = [
	createTextBotMsg('The light messenger enters the dialogue and serves you!', 'system'),
	createTextBotMsg("Hello, I am a robot, I have a good memory. Can you tell me your name?"),
];

function initNavBar() {
	return {
		title: 'Rasa Assistant'
	}
}

export function initBotConfig() {
	return {
		avatar: botAvatar
	}
}

function initUserConfig() {
	return {
		avatar: userAvatar
	}
}


export const BotConfig = {
	navbar: initNavBar(),
	robot: initBotConfig(),
	user: initUserConfig(), 	// 用户头像
	messages: initialMessages,
	quickReplies: defaultQuickReplies,//快捷短语
	placeholder: 'Input...', // 输入框占位符
	toolbar: [
		{
			type: 'image',
			icon: 'image',
			title: '相册',
		},
	],
}
