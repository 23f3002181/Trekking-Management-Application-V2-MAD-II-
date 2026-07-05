<template>
    <div>
        <div class="d-flex justify-content-between mb-4 gap-3">

            <input type="text" class="form-control shadow-sm border-0" placeholder="Search treks by name or location..."
                :value="trekStore.searchQuery" @input="onSearchInput">

            <select class="form-select w-auto shadow-sm border-0" :value="trekStore.filterDifficulty"
                @change="onFilterChange">
                <option value="">Difficulty: All</option>
                <option value="Easy">Easy</option>
                <option value="Moderate">Moderate</option>
                <option value="Hard">Hard</option>
            </select>

        </div>

        <div class="row g-4">
            <div class="col-md-4" v-for="trek in availableTreks" :key="trek.id">
                <div class="card h-100 shadow-sm border-0">
                    <img :src="trek.image_url" class="card-img-top" alt="Trek" style="height: 180px; object-fit: cover;">
                    <div class="card-body">
                        <h6 class="card-title fw-bold">{{ trek.name }}</h6>
                        <p class="text-muted small mb-2">{{ trek.location }}</p>
                        <p class="small mb-2">{{ trek.difficulty }} - {{ trek.duration }} Days</p>
                        <p class="small text-danger fw-bold">Slots Left: {{ trek.slots }}</p>
                        <button @click="bookTrek(trek)" class="btn btn-success w-100 shadow-sm">Book Now</button>
                    </div>
                </div>
            </div>
        </div>

        <div class="d-flex justify-content-center mt-5" v-if="totalPages > 1">
            <ul class="pagination">

                <li class="page-item" :class="{ disabled: currentPage === 1 }">
                    <button class="page-link" @click="changePage(currentPage - 1)">&lt;</button>
                </li>

                <li class="page-item" v-for="page in totalPages" :key="page" :class="{ active: currentPage === page }">
                    <button class="page-link" @click="changePage(page)">{{ page }}</button>
                </li>

                <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                    <button class="page-link" @click="changePage(currentPage + 1)">&gt;</button>
                </li>

            </ul>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { useTrekStore } from '../../stores/trekStore'
import { useToast } from "vue-toastification"
import Swal from 'sweetalert2'

export default {
    setup() {
        const trekStore = useTrekStore();
        const toast = useToast();
        return { trekStore, toast };
    },
    data() {
        return {
            availableTreks: [],
            totalPages: 1,
            searchTimeout: null
        }
    },
    mounted() {
        // When the component loads, it will use whatever is saved in the store!
        this.fetchOpenTreks()
    },
    methods: {
        async fetchOpenTreks() {
            try {
                const res = await axios.get('http://127.0.0.1:5000/api/user/treks', {
                    params: {
                        // Pull parameters directly from Pinia memory
                        search: this.trekStore.searchQuery,
                        difficulty: this.trekStore.filterDifficulty,
                        page: this.trekStore.currentPage,
                        per_page: 6
                    }
                })
                this.availableTreks = res.data.treks
                this.trekStore.currentPage = res.data.current_page
                this.totalPages = res.data.total_pages || 1
            } catch (err) {
                console.error("Error fetching treks", err)
            }
        },

        // THE DEBOUNCED SEARCH
        onSearchInput(event) {
            // 1. Update the store memory
            this.trekStore.updateSearch(event.target.value);

            // 2. Clear the previous timer if they are still typing
            clearTimeout(this.searchTimeout);

            // 3. Set a new timer to wait 400ms before calling the backend
            this.searchTimeout = setTimeout(() => {
                this.fetchOpenTreks();
            }, 400);
        },

        onFilterChange(event) {
            this.trekStore.updateDifficulty(event.target.value);
            this.fetchOpenTreks();
        },

        changePage(pageNumber) {
            if (pageNumber >= 1 && pageNumber <= this.totalPages) {
                this.trekStore.setPage(pageNumber);
                this.fetchOpenTreks();
            }
        },
        async bookTrek(trek) {
            const result = await Swal.fire({
                title: `Book ${trek.name}?`,
                text: `Are you sure you want to reserve a slot for this trek?`,
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#198754', // Success green
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Yes, book it!'
            });

            if (result.isConfirmed) {
                try {
                    await axios.post(`http://127.0.0.1:5000/api/user/book/${trek.id}`)

                    this.toast.success("Trek booked successfully!")
                    // Refresh the list so the available slots decrement instantly
                    this.fetchOpenTreks()
                } catch (err) {
                    this.toast.error(err.response?.data?.message || 'Error booking trek.')
                }
            }
        }
    }
}
</script>