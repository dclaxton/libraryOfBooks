<template>
    <div ckass="container">
      <div class="row">
        <div class="col-9">
          <h1>Books</h1>
        </div>
        <div class="col-2 text-center my-auto">
          <div>
            <b-button variant="outline-primary">Add book</b-button>
          </div>
        </div>
      </div>
      <div class="row">
        <table class="table table-hover">
          <thead>
            <th scope="col">Title</th>
            <th scope="col">Author</th>
            <th scope="col">Previously Read</th>
            <th scope="col">Available in Library</th>
            <th></th>
          </thead>
          <tbody>
            <tr v-for="(book,index) in books" :key="index">
              <td>{{book.name}}</td>
              <td>{{book.author}}</td>
              <td>
                <span v-if="book.has_read">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <span v-if="book.available">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <b-button-group size="sm">
                  <b-button variant="outline-warning">Edit</b-button>
                  <b-button variant="outline-danger" @click="onRemoveBook(book)">Delete</b-button>
                </b-button-group>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'BookItem',
  data () {
    return {
      books: []
    }
  },
  methods: {
    getAllBooks () {
      axios.get('http://localhost:5000/books')
        .then((res) => {
          this.books = res.data
        })
    },
    removeBook (bookID) {
      const path = `http://localhost:5000/books/${bookID}`
      axios.delete(path)
        .then(() => {
          this.getAllBooks()
        })
    },
    onRemoveBook (book) {
      this.removeBook(book.id)
    }
  },
  created () {
    this.getAllBooks()
  }
}
</script>
