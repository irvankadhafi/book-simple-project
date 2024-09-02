<template>
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">Delete Book</h1>
      <div class="max-w-md mx-auto bg-white p-6 rounded-lg shadow-lg">
        <p class="text-gray-700 text-lg mb-4">Are you sure you want to delete the book titled "{{ book.title }}"?</p>
        <div class="flex justify-center">
          <button @click="deleteBook" class="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg shadow-lg focus:outline-none focus:ring-2 focus:ring-red-500">Delete Book</button>
        </div>
      </div>
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
      const book = ref({});
  
      const fetchBook = async () => {
        try {
          const response = await axios.get(`http://localhost:8000/api/v1/books/${route.params.id}`);
          book.value = response.data.data;
        } catch (error) {
          console.error('Error fetching book:', error);
        }
      };
  
      const deleteBook = async () => {
        try {
          await axios.delete(`http://localhost:8000/api/v1/books/${route.params.id}`);
          router.push('/');
        } catch (error) {
          console.error('Error deleting book:', error);
        }
      };
  
      onMounted(fetchBook);
  
      return { book, deleteBook };
    }
  };
  </script>
  