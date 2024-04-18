import { readQ_Alpha, powerMod, computeXa,computeYa } from "./utilities.js";
import User from "../backend/models/userModel.js";

const usertKeys = async (my_id) => {
  let Xa = computeXa("diffieHelman.txt");
  let Ya = computeYa(Xa,"diffieHelman.txt");
    const updateData = { diffieHelman_Xa: Xa, diffieHelman_Ya: Ya }; // Update data

  await User.findByIdAndUpdate(my_id, updateData ,{ upsert: true });
};

const secretKey = async (my_id, friend_id) => {
  let { q, alpha } = readQ_Alpha("diffieHelman.txt");
  let friend = await User.findById(friend_id);
  let me = await User.findById(my_id);
  let Yb = friend.diffieHelman_Ya;
  let Xa = me.diffieHelman_Xa;
    let K = powerMod(Yb, Xa, q);
    console.log(q,alpha,Yb,Xa,K)
  return K;
};

export { usertKeys, secretKey };
