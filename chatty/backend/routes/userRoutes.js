import express from "express";
import {
  loginUser,
  logoutUser,
  signupUser,
  getUserProfile,
} from "../controllers/userController.js";


const router = express.Router();


router.post("/signup", signupUser);
router.post("/login", loginUser);
router.post("/logout", logoutUser);
router.get("/profile/:query", getUserProfile);

export default router;
