<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">Create Book</h1>
    <form @submit.prevent="createBook" class="max-w-md mx-auto">
      <div class="mb-4">
        <label for="title" class="block text-gray-700">Title:</label>
        <input v-model="book.title" id="title" type="text" class="p-3 border border-gray-300 rounded-lg w-full" required />
      </div>
      <div class="mb-4">
        <label for="author" class="block text-gray-700">Author:</label>
        <input v-model="book.author" id="author" type="text" class="p-3 border border-gray-300 rounded-lg w-full" required />
      </div>
      <div class="mb-4">
        <label for="published_date" class="block text-gray-700">Published Date:</label>
        <input v-model="book.published_date" id="published_date" type="date" class="p-3 border border-gray-300 rounded-lg w-full" required />
      </div>
      <div class="mb-4">
        <label for="isbn" class="block text-gray-700">ISBN:</label>
        <input v-model="book.isbn" id="isbn" type="text" class="p-3 border border-gray-300 rounded-lg w-full" required />
      </div>
      <div class="mb-4">
        <label for="pages" class="block text-gray-700">Pages:</label>
        <input v-model="book.pages" id="pages" type="number" class="p-3 border border-gray-300 rounded-lg w-full" required />
      </div>
      <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg shadow-lg">Create</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';

export default {
  name: 'CreateBook',
  setup() {
    const book = ref({
      title: '',
      author: '',
      published_date: '',
      isbn: '',
      pages: '',
    });

    const createBook = async () => {
      try {
        await axios.post('http://localhost:8000/api/v1/books/', book.value);
        alert('Book created successfully!');
        window.location.href = '/';
      } catch (error) {
        alert('Failed to create book.');
        console.error(error);
      }
    };

    return { book, createBook };
  },
};
</script>
