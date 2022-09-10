
<template>
    <div ckass="container">
      <div class="row">
        <div class="col-9">
          <h1>Books</h1>
        </div>
        <div class="col-2 text-center my-auto">
          <div>
            <b-button variant="outline-primary" v-b-modal.book-modal>Add book</b-button>
          </div>
        </div>
      </div>
      <div class="row">
        <b-table :items="books" :fields="fields">
          <template #cell(name)="data">
            <b-form-input v-if="books[data.index].isEdit" type="text" v-model="books[data.index].name"></b-form-input>
            <span v-else>{{data.value}}</span>
          </template>
          <template #cell(author)="data">
            <b-form-input v-if="books[data.index].isEdit" v-model="books[data.index].author"></b-form-input>
            <span v-else>{{data.value}}</span>
          </template>
          <template #cell(hasRead)="data">
            <b-form-select v-if="books[data.index].isEdit" v-model="books[data.index].hasRead" :options="['true', 'false']"></b-form-select>
            <span v-else> <span v-if="data.value">Yes</span>
              <span v-else>No</span></span>
          </template>
          <template #cell(available)="data">
            <b-form-select v-if="books[data.index].isEdit" v-model="books[data.index].available" :options="['true', 'false']"></b-form-select>
            <span v-else><span v-if="data.value">Yes</span>
            <span v-else>No</span></span>
          </template>
          <template #cell(edit)="data">
            <b-button-group>
              <b-button size="sm" variant="warning" @click="editRow(data)">
                <span v-if="!books[data.index].isEdit">Edit</span>
                <span v-else>Done</span>
              </b-button>
              <b-button size="sm" variant="danger" @click="removeBook(data)">Remove</b-button>
            </b-button-group>
          </template>
        </b-table>
        <!-- <pre>
          {{books}}
        </pre> -->
      </div>
      <b-modal ref="addBookModal" id="book-modal" title="Add a new book" hide-footer>
        <b-form @submit="onSubmit" @reset="onReset" class="w-100">
          <b-form-group id="form-name-group" label="Name:" label-for="form-name-input">
            <b-form-input id="form-name-input" type="text" v-model="addBookForm.name" required placeholder="Enter book name">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-author-group" label="Author:" label-for="form-author-input">
            <b-form-input id="form-author-input" type="text" v-model="addBookForm.author" required placeholder="Enter author">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-read-group">
            <b-form-checkbox-group v-model="addBookForm.read" id="form-checks">
              <b-form-checkbox value="true">Read?</b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>
          <b-form-group id="form-avail-group">
            <b-form-checkbox-group v-model="addBookForm.available" id="form-checks">
              <b-form-checkbox value="true">Available?</b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>
          <b-button type="submit" variant="primary">Submit</b-button>
        </b-form>
      </b-modal>
    </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'BookItem',
  data () {
    return {
      fields: [
        { key: 'name', label: 'Name' },
        { key: 'author', label: 'Author' },
        { key: 'hasRead', label: 'Previously Read' },
        { key: 'available', label: 'Available in Library' },
        { key: 'edit', label: '' }
      ],
      books: [],
      addBookForm: {
        name: '',
        author: '',
        read: [],
        available: []
      }
    }
  },
  created () {
    this.books = this.getAllBooks()
  },
  methods: {
    getAllBooks () {
      axios.get('http://localhost:5000/books')
        .then((res) => {
          this.books = res.data
        })
    },
    removeBook (data) {
      const path = `http://localhost:5000/books/${data.item.id}`
      axios.delete(path)
        .then(() => {
          this.books.splice(data.index, 1)
        })
    },
    editRow (data) {
      this.books = this.books.map(item => ({ ...item, isEdit: this.books[data.index] ? this.books[data.index].isEdit : false }))
      this.books[data.index].isEdit = !this.books[data.index].isEdit
      console.log(this.books[data.index].isEdit + ' ' + data.index + ' ' + !this.books[data.index].isEdit)
      if (this.books[data.index].isEdit === false) {
        this.books = this.books.map(item => ({ ...item, isEdit: false }))
        axios.put(`http://localhost:5000/books/${data.item.id}`, {
          name: data.item.name,
          author: data.item.author,
          hasRead: data.item.hasRead,
          available: data.item.available
        })
        this.getBooks()
      }
    },
    addBook (payload) {
      console.log(payload)
      const path = 'http://localhost:5000/books'
      axios.post(path, payload)
        .then(() => {
          this.getBooks()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.getAllBooks()
        })
    },
    onSubmit (evt) {
      evt.preventDefault()
      this.$refs.addBookModal.hide()
      let read = false
      let available = false
      if (this.addBookForm.read[0]) read = true
      if (this.addBookForm.available[0]) available = true
      const payload = {
        name: this.addBookForm.name,
        author: this.addBookForm.author,
        hasRead: read,
        available
      }
      this.addBook(payload)
      this.resetAddBookForm()
    },
    onReset (evt) {
      evt.preventDefault()
      this.$refs.addBookModal.hide()
      this.getAllBooks()
      this.resetAddBookForm()
    },
    resetAddBookForm () {
      this.addBookForm.name = ''
      this.addBookForm.author = ''
      this.addBookForm.read = []
      this.addBookForm.available = []
    }
  }
}
</script>
