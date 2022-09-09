<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="#">Library</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
      </b-collapse>
    </b-navbar>
    <div class="container-fluid">
      <div class="row justify-content-center">
        <div class="col-6">
          <BookItem/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BookItem from './components/BookItem.vue'

export default {
  name: 'App',
  components: {
    BookItem
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
