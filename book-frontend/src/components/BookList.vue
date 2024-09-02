<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">Book Collection</h1>

    <div class="flex flex-col md:flex-row md:justify-between items-center mb-6 space-y-4 md:space-y-0">
      <input
        v-model="searchQuery"
        @input="fetchBooks"
        type="text"
        placeholder="Search books..."
        class="p-3 border border-gray-300 rounded-lg w-full md:w-1/2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <select
        v-model="sortOption"
        @change="fetchBooks"
        class="border border-gray-300 rounded-lg p-3 mt-4 md:mt-0 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">Sort By</option>
        <option value="title:asc">Title (A-Z)</option>
        <option value="title:desc">Title (Z-A)</option>
        <option value="author:asc">Author (A-Z)</option>
        <option value="author:desc">Author (Z-A)</option>
        <option value="published_date:asc">Published Date (Earliest)</option>
        <option value="published_date:desc">Published Date (Latest)</option>
      </select>
      <button
        @click="goToCreate"
        class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        Create Book
      </button>
    </div>

    <div v-if="books.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div
        v-for="book in books"
        :key="book.id"
        class="bg-white p-6 border border-gray-200 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200"
      >
        <h2 class="text-2xl font-semibold text-gray-700">{{ book.title }}</h2>
        <p class="text-gray-500 mt-2">Author: {{ book.author }}</p>
        <p class="text-gray-500">Published Date: {{ new Date(book.published_date).toLocaleDateString() }}</p>
        <div class="mt-4 flex justify-between">
          <button
            @click="goToDetail(book.id)"
            class="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-lg shadow-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            Details
          </button>
          <button
            @click="goToUpdate(book.id)"
            class="bg-yellow-600 hover:bg-yellow-700 text-white font-semibold py-2 px-4 rounded-lg shadow-lg focus:outline-none focus:ring-2 focus:ring-yellow-500"
          >
            Update
          </button>
          <button
            @click="deleteBook(book.id)"
            class="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg shadow-lg focus:outline-none focus:ring-2 focus:ring-red-500"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
    <p v-else class="text-center text-gray-500">No books found</p>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const searchQuery = ref('');
    const sortOption = ref('');
    const books = ref([]);
    const router = useRouter();

    const fetchBooks = async () => {
      const params = new URLSearchParams();
      
      if (searchQuery.value) {
        params.append('query', searchQuery.value);
      }
      
      if (sortOption.value) {
        params.append('sort', sortOption.value);
      }

      params.append('page', 1);
      params.append('size', 10);

      try {
        const response = await axios.get(`http://localhost:8000/api/v1/books/?${params.toString()}`);
        books.value = response.data.data.items;
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    };

    const goToCreate = () => {
      router.push('/create');
    };

    const goToDetail = (id) => {
      router.push(`/detail/${id}`);
    };

    const goToUpdate = (id) => {
      router.push(`/update/${id}`);
    };

    const deleteBook = async (id) => {
      try {
        await axios.delete(`http://localhost:8000/api/v1/books/${id}`);
        fetchBooks(); // Refresh the book list
      } catch (error) {
        console.error('Error deleting book:', error);
      }
    };

    onMounted(() => {
      fetchBooks();
    });

    return {
      searchQuery,
      sortOption,
      books,
      fetchBooks,
      goToCreate,
      goToDetail,
      goToUpdate,
      deleteBook,
    };
  },
};
</script>
