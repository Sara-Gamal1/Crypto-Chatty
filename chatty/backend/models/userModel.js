import mongoose from "mongoose";

const userSchema = mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
    },
    username: {
      type: String,
      required: true,
      unique: true,
    },
    password: {
      type: String,
      minLength: 6,
      required: true,
    },
    algamal_Xa: {
      type: BigInt,
    },
    algamal_Ya: {
      type: BigInt,
    },
    diffieHelman_Xa: {
      type: BigInt,
    },
    diffieHelman_Ya: {
      type: BigInt,
    },
  },
  {
    timestamps: true,
  }
);

const User = mongoose.model("User", userSchema);

export default User;
