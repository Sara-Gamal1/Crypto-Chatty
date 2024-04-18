import { getDigitalSignature, verifyDigitalSignature } from "./algamal.js";
import { usertKeys, secretKey } from "./diffieHelman.js";

import connectDB from "../backend/db/connectDB.js";

await connectDB();

// let { S1, S2 } = await getDigitalSignature(123, "66211b6cb9e77ab1446edd3c");
// console.log(
//   await verifyDigitalSignature(123, S1, S2, "66211b6cb9e77ab1446edd3c")
// );

await usertKeys("66211b6cb9e77ab1446edd3c");
await usertKeys("66211b7fb9e77ab1446edd43");

let k1 = await secretKey(
  "66211b6cb9e77ab1446edd3c",
  "66211b7fb9e77ab1446edd43"
);

let k2 = await secretKey(
  "66211b7fb9e77ab1446edd43",
  "66211b6cb9e77ab1446edd3c"
);

console.log(k1, k2, k1 == k2);
