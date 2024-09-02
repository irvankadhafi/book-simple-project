<template>
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">Book Details</h1>
      <div class="max-w-md mx-auto p-4 border border-gray-300 rounded-lg">
        <div class="mb-4">
          <strong class="text-gray-700">Title:</strong>
          <p>{{ book.title }}</p>
        </div>
        <div class="mb-4">
          <strong class="text-gray-700">Author:</strong>
          <p>{{ book.author }}</p>
        </div>
        <div class="mb-4">
          <strong class="text-gray-700">Published Date:</strong>
          <p>{{ book.published_date }}</p>
        </div>
        <div class="mb-4">
          <strong class="text-gray-700">ISBN:</strong>
          <p>{{ book.isbn }}</p>
        </div>
        <div class="mb-4">
          <strong class="text-gray-700">Pages:</strong>
          <p>{{ book.pages }}</p>
        </div>
        <div class="flex justify-end">
          <button @click="goToUpdate" class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg shadow-lg mr-2">Edit</button>
          <button @click="deleteBook" class="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg shadow-lg">Delete</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'BookDetail',
    props: ['id'],
    setup(props) {
      const book = ref({});
      const router = useRouter();
  
      onMounted(async () => {
        try {
          const response = await axios.get(`http://localhost:8000/api/v1/books/${props.id}`);
          book.value = response.data.data;
        } catch (error) {
          console.error(error);
        }
      });
  
      const goToUpdate = () => {
        router.push(`/update/${props.id}`);
      };
  
      const deleteBook = async () => {
        try {
          await axios.delete(`http://localhost:8000/api/v1/books/${props.id}`);
          alert('Book deleted successfully!');
          router.push('/');
        } catch (error) {
          alert('Failed to delete book.');
          console.error(error);
        }
      };
  
      return { book, goToUpdate, deleteBook };
    },
  };
  </script>
  