import {
  hash,
  generateRandomK,
  modInverse,
  getXa,
  getYa,
  readQ_Alpha,
  powerMod,
} from "./utilities.js";

const getDigitalSignature = async (M, my_id) => {
  let m = BigInt(hash(toString(M)));
  let Xa = await getXa(my_id);
  let { q, alpha } = readQ_Alpha("gamal.txt");
  let k = generateRandomK(q);
  let S1 = BigInt(powerMod(alpha, k, q));

  let kInverse = BigInt(modInverse(k, q - 1n));
  let S2 = BigInt((kInverse * (m - Xa * S1)) % (q - 1n));
  console.log(m, Xa, q, alpha, k,kInverse, S1, S2);
  return { S1, S2 };
};

const verifyDigitalSignature = async (M, S1, S2, friend_id) => {
  let m = BigInt(hash(toString(M)));
  let Yb = await getYa(friend_id);
  let { q, alpha } = readQ_Alpha("gamal.txt");
  let V1 = BigInt(powerMod(alpha, m, q));
  let temp1 = BigInt(powerMod(Yb, S1, q));
  let temp2 = BigInt(powerMod(S1, S2, q));
  let V2 = BigInt((temp1 * temp2) % q);

  console.log(m, Yb, q, alpha, V1, V2, temp1, temp2);;
  return V1 == V2;
};

export { getDigitalSignature, verifyDigitalSignature };
