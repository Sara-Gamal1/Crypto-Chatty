import Conversation from "../models/conversationModel.js";
import Message from "../models/messageModel.js";
import { getRecipientSocketId, io } from "../socket/socket.js";
import aes256 from "aes256";
async function sendMessage(req, res) {
  try {
    const { recipientId, message } = req.body;

    const senderId = req.user._id;

    let conversation = await Conversation.findOne({
      participants: { $all: [senderId, recipientId] },
    });

    let key = "it is a bad day not a bad life";
    let encryptedMsg = aes256.encrypt(key, message);

    if (!conversation) {
      conversation = new Conversation({
        participants: [senderId, recipientId],
        lastMessage: {
          text: encryptedMsg,
          sender: senderId,
        },
      });
      await conversation.save();
    }
    const originalMessage = new Message({
      conversationId: conversation._id,
      sender: senderId,
      text: message,
    });

    const newMessage = new Message({
      conversationId: conversation._id,
      sender: senderId,
      text: encryptedMsg,
    });

    await Promise.all([
      newMessage.save(),
      conversation.updateOne({
        lastMessage: {
          text: encryptedMsg,
          sender: senderId,
        },
      }),
    ]);

    const recipientSocketId = getRecipientSocketId(recipientId);
    if (recipientSocketId) {
      io.to(recipientSocketId).emit("newMessage", newMessage);
    }

    res.status(201).json(originalMessage);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}

async function getMessages(req, res) {
  const { otherUserId } = req.params;
  const userId = req.user._id;
  try {
    const conversation = await Conversation.findOne({
      participants: { $all: [userId, otherUserId] },
    });

    if (!conversation) {
      return res.status(404).json({ error: "Conversation not found" });
    }

    const messages = await Message.find({
      conversationId: conversation._id,
    }).sort({ createdAt: 1 });

    let key = "it is a bad day not a bad life";
    let decryptedMessages = messages.map((msg) => {
      msg.text = aes256.decrypt(key, msg.text);
      return msg;
    });

    res.status(200).json(decryptedMessages);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}

async function getConversations(req, res) {
  const userId = req.user._id;
  try {
    let conversations = await Conversation.find({
      participants: userId,
    }).populate({
      path: "participants",
      select: "username",
    });

    // remove the current user from the participants array
    conversations.forEach((conversation) => {
      conversation.participants = conversation.participants.filter(
        (participant) => participant._id.toString() !== userId.toString()
      );
    });

    let key = "it is a bad day not a bad life";
    conversations.forEach((conversation) => {
      try {
        conversation.lastMessage.text = aes256.decrypt(
          key,
          conversation.lastMessage.text
        );
      } catch (error) {
        console.error("Error decrypting message:", error);
      }
    });
    res.status(200).json(conversations);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}

export { sendMessage, getMessages, getConversations };
