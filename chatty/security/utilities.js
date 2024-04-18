import User from "../backend/models/userModel.js";
import fs from "fs";
import { sha1 } from "js-sha1";

const readQ_Alpha = (fileName) => {
  // const lines = fs.readFileSync("C:\Users\LAPTOP\Desktop\chatty\security\Qalpha.txt", "utf-8").split("\n");
  // // Parse the numbers from the lines
  // const q = parseInt(lines[0].trim(), 10); // Assuming the first number is on the first line
  // const alpha = parseInt(lines[1].trim(), 10); // Assuming the second number is on the second line
  let q = BigInt(29);
  let alpha = BigInt(2);
  return { q, alpha };
};

const decimalToBinary = (decimal) => {
  return decimal.toString(2); // Convert decimal to binary
};

const modInverse = (a, m) => {
  for (let x = 1n; x < m; x++) if (((a % m) * (x % m)) % m == 1) return x;
};

const gcd = (a, b) => {
  while (b !== 0n) {
    let temp = b;
    b = a % b;
    a = temp;
  }
  return a;
};
const hash = (M) => {
  sha1(M);
  let hash = sha1.create();
  hash.update(M);
  let hexHash = hash.hex();
  let decimalHash = parseInt(hexHash, 16); // Convert hexadecimal to decimal
  return decimalHash;
};

const generateRandomK = (q) => {
  let K;
  do {
    // Generate a random integer in the range [1, q-1]
    K = BigInt(Math.floor(Math.random() * Number(q - 1n) + 1));
  } while (gcd(K, q - 1n) !== 1n); // Check if gcd(K, q - 1) = 1
  return K;
};
const getXa = async (id) => {
  let user = await User.findById(id);
  return user.algamal_Xa;
};
const getYa = async (id) => {
  let user = await User.findById(id);
  return user.algamal_Ya;
};

const powerMod = (a, b, n) => {
  let f = 1n;
  let binary = decimalToBinary(b);
  let k = binary.length;
  for (let i = 0; i <k; i++) {
    f = (f * f) % n;

    if (binary[i] == "1") {
      f = (f * a) % n;
    }
  }
  return f;
};

const computeXa = (fileName) => {
  let { q, alpha } = readQ_Alpha(fileName);
  let xa = BigInt(Math.floor(Math.random() * Number(q - 3n) + 2));

  return xa;
};

const computeYa = (xa, fileName) => {
  let { q, alpha } = readQ_Alpha(fileName);
  let ya = BigInt(alpha ** xa % q);
  return ya;
};

export {
  readQ_Alpha,
  decimalToBinary,
  modInverse,
  gcd,
  hash,
  generateRandomK,
  getXa,
  getYa,
  powerMod,
  computeXa,
  computeYa,
};
