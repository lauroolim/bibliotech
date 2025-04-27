import { Book } from "../model/book";
import { Response, Request } from "express";
import { pool } from "../../db";

export class BookController {
  private book: Book;

  constructor() {
    this.book = new Book(pool);
  }

  async displayBooks(req: Request, res: Response) {
    try {
      const books = await this.book.getAll();
      res.render("books/index", { books });
    } catch (err) {
      console.error("erro no display dos livros" + err);
      res.status(500).render("error", {
        message:
          "Erro interno do servidor ao renderizar livros, tente mais tarde...",
      });
    }
  }
}
