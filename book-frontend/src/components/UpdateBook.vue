<template>
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">Update Book</h1>
      <form @submit.prevent="updateBook" class="max-w-md mx-auto bg-white p-6 rounded-lg shadow-lg">
        <div class="mb-4">
          <label for="title" class="block text-gray-700 text-sm font-semibold mb-2">Title</label>
          <input v-model="book.title" type="text" id="title" placeholder="Enter book title" class="w-full p-2 border border-gray-300 rounded-lg" required />
        </div>
        <div class="mb-4">
          <label for="author" class="block text-gray-700 text-sm font-semibold mb-2">Author</label>
          <input v-model="book.author" type="text" id="author" placeholder="Enter author's name" class="w-full p-2 border border-gray-300 rounded-lg" required />
        </div>
        <div class="mb-4">
          <label for="published_date" class="block text-gray-700 text-sm font-semibold mb-2">Published Date</label>
          <input v-model="book.published_date" type="date" id="published_date" class="w-full p-2 border border-gray-300 rounded-lg" required />
        </div>
        <div class="mb-4">
          <label for="isbn" class="block text-gray-700 text-sm font-semibold mb-2">ISBN</label>
          <input v-model="book.isbn" type="text" id="isbn" placeholder="Enter ISBN" class="w-full p-2 border border-gray-300 rounded-lg" required />
        </div>
        <div class="mb-4">
          <label for="pages" class="block text-gray-700 text-sm font-semibold mb-2">Number of Pages</label>
          <input v-model="book.pages" type="number" id="pages" placeholder="Enter number of pages" class="w-full p-2 border border-gray-300 rounded-lg" required />
        </div>
        <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">Update Book</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { ref, onMounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  
  export default {
    setup() {
      const route = useRoute();
      const router = useRouter();
      const book = ref({
        title: '',
        author: '',
        published_date: '',
        isbn: '',
        pages: '',
      });
  
      const fetchBook = async () => {
        try {
          const response = await axios.get(`http://localhost:8000/api/v1/books/${route.params.id}`);
          book.value = response.data.data;
        } catch (error) {
          console.error('Error fetching book:', error);
        }
      };
  
      const updateBook = async () => {
        try {
          await axios.put(`http://localhost:8000/api/v1/books/${route.params.id}`, book.value);
          router.push('/');
        } catch (error) {
          console.error('Error updating book:', error);
        }
      };
  
      onMounted(fetchBook);
  
      return { book, updateBook };
    }
  };
  </script>
  