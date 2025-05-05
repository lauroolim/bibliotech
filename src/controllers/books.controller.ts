import { Book } from "../model/book";
import express, { Request, Response } from "express";
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

  async displayFormAddBook(req: Request, res: Response) {
    try {
      res.render("books/add");
    } catch (err) {
      console.error("erro no display do formulario de adicionar livros" + err);
      res.status(500).render("error", {
        message:
          "Erro interno do servidor ao renderizar formulario de adicionar livros, tente mais tarde...",
      });
    }
  }

  async displayOneBook(req: Request, res: Response) {
    try {
      const { id } = req.params;

      if (!id || isNaN(Number(id))) {
        return res.status(400).render("error", {
          message: "ID nao indentificado ou invalido",
        });
      }

      const books = await this.book.getOne(Number(id));

      if (!books) {
        return res.status(404).render("error", {
          message: "Livro nao encontrado",
        });
      }

      res.render("books/detail", { books });
    } catch (err) {
      console.error("erro no display dos livros" + err);
      res.status(500).render("error", {
        message:
          "Erro interno do servidor ao renderizar livros, tente mais tarde...",
      });
    }
  }

  async insertBooks(req: Request, res: Response) {
    try {
      if(!req.body){
        return res.status(400).render("error", {
          message: "Nenhum dado foi recebido",
        });
      }
      const { title, author } = req.body;

      const insert = await this.book.create(title, author);
      res.redirect("/books");
    } catch (err) {
      console.error("falha ao inserir livro " + err);
      res.sendStatus(500).render("error", {
        message:
          "Erro interno do servidor ao inserir livros, tente mais tarde...",
      });
    }
  }
}
