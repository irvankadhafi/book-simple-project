import { createRouter, createWebHistory } from 'vue-router';
import BookList from '../components/BookList.vue';
import CreateBook from '../components/CreateBook.vue';
import UpdateBook from '../components/UpdateBook.vue';
import BookDetail from '../components/BookDetail.vue';


const routes = [
  { path: '/', name: 'BookList', component: BookList },
  { path: '/create', name: 'CreateBook',  component: CreateBook },
  { path: '/update/:id', name: 'UpdateBook', component: UpdateBook, props: true },
  { path: '/detail/:id', name: 'BookDetail', component: BookDetail, props: true },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
