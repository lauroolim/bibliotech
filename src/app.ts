import express, { Request, Response } from "express";
import path from "path";
import session from "express-session";
import booksRoutes from "./routes/books.route";
const app = express();
const PORT = 3000;

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "../views"));

app.use(
  session({
    secret: "developm",
    resave: false,
    saveUninitialized: true,
  }),
);

declare module "express-session" {
  interface SessionData {
    user?: {
      id: number;
      username: string;
      email: string;
    };
  }
}

app.use("/books", booksRoutes);

app.get("/", (req, res) => {
  res.render("home", { user: req.session.user });
});

app.listen(PORT, () => {
  console.log("app rodando na porta 3000");
});
