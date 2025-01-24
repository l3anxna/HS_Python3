import { exec } from "child_process";
import path from "path";
import type { NextApiRequest, NextApiResponse } from "next";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === "POST") {
    const { date, steps, calories } = req.body;

    const scriptPath = path.join(process.cwd(), "scripts", "tracker.py");
    const command = `python3 ${scriptPath} ${date} ${steps} ${calories}`;
    
    exec(command, (error, stdout, stderr) => {
      if (error) {
        return res.status(500).json({ error: stderr });
      }
      return res.status(200).json({ message: stdout.trim() });
    });
  } else if (req.method === "GET") {
    const scriptPath = path.join(process.cwd(), "scripts", "read_data.py");
    exec(`python3 ${scriptPath}`, (error, stdout, stderr) => {
      if (error) {
        return res.status(500).json({ error: stderr });
      }
      return res.status(200).json({ data: JSON.parse(stdout) });
    });
  } else {
    res.status(405).json({ message: "Method Not Allowed" });
  }
}
