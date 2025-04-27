import { Router } from "express";
import { BookController } from "../controllers/books.controller";

const rt = Router();
const bkcontroller = new BookController();

rt.get("/", (req, res) => bkcontroller.displayBooks(req, res));

export default rt;
