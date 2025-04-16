import express, { response } from "express";
import "dotenv/config";
import { rateLimit } from "express-rate-limit";
import { createClient } from "@supabase/supabase-js";
import * as crypto from "crypto";

const app = express();

// 1000 requests per 5 minutes
const limiter = rateLimit({
  windowMs: 5 * 60 * 1000,
  limit: 1000,
  standardHeaders: "draft-8",
  legacyHeaders: false,
});
app.use(limiter);

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY,
  { db: { schema: "dev" } }
); // for dev use only
// const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY); // reminder to idiotbuildr uncomment this before pushing to prod

async function hashString(str) {
  const encoder = new TextEncoder();
  const data = encoder.encode(str);
  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray
    .map((byte) => byte.toString(16).padStart(2, "0"))
    .join("");
  return hashHex;
}

async function validateAuth(key) {
  const keyHash = await hashString(key);

  const { data, error } = await supabase
    .from("auth")
    .select()
    .eq("keyHash", keyHash);

  if (error) {
    throw Error(error);
  } else if (data.length >= 1) {
    return data[0];
  } else {
    return null;
  }
}

app.get("/events", async (req, res) => {
  const { data, error } = await supabase.from("events").select();

  if (error) {
    res.status = 500;
    res.send("500 Internal Server Error");
    console.error(error);
  } else {
    let l = [];

    for (const event of data) {
      l.push({
        key: event.key,
        organizer: event.organizerId,
        title: event.title,
        subtitle: event.subtitle,
        description: event.description,
        image: event.image,
        address: {
          street: event.addressStreet,
          city: event.addressCity,
          state: event.addressState,
        },
        coordinates: {
          lat: event.coordsLat,
          lon: event.coordsLon,
        },
        startTime: event.startTime,
        endTime: event.endsTime,
      });
    }

    res.send(l);
  }
});

app.get("/eventInfo", async (req, res) => {
  const query = req.query.key;

  if (query) {
    const { data, error } = await supabase
      .from("events")
      .select()
      .eq("key", query);

    if (error) {
      res.statusCode = 500;
      res.send("500 Internal Server Error");
      console.error(error);
    } else if (data.length >= 1) {
      res.send({
        key: data[0].key,
        organizer: data[0].organizerId,
        title: data[0].title,
        subtitle: data[0].subtitle,
        description: data[0].description,
        image: data[0].image,
        address: {
          street: data[0].addressStreet,
          city: data[0].addressCity,
          state: data[0].addressState,
        },
        coordinates: {
          lat: data[0].coordsLat,
          lon: data[0].coordsLon,
        },
        startTime: data[0].startTime,
        endTime: data[0].endsTime,
      });
    } else {
      res.send(`No event with key ${query} was found.`);
    }
  } else {
    res.send("Please provide a key of an event.");
  }
});

app.listen(process.env.PORT);
