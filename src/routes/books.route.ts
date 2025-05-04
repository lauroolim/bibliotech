import { Router } from "express";
import { BookController } from "../controllers/books.controller";

const rt = Router();
const bkcontroller = new BookController();

rt.get("/", (req, res) => bkcontroller.displayBooks(req, res));
rt.get("/:id", (req, res) => bkcontroller.displayOneBook(req, res));
rt.post("/", (req, res) => bkcontroller.insertBooks(req, res));
rt.get("/add", (req, res) => bkcontroller.displayFormAddBook(req, res));

export default rt;
