import { Router } from "express";
import { BookController } from "../controllers/books.controller";

const rt = Router();
const bkcontroller = new BookController();

rt.get("", (req, res) => bkcontroller.displayBooks(res));
rt.get("/form/add", (req, res) => bkcontroller.displayFormAddBook(res));
rt.get("/:id", (req, res) => bkcontroller.displayOneBook(req, res));
rt.post("", (req, res) => bkcontroller.insertBooks(req, res));


export default rt;
