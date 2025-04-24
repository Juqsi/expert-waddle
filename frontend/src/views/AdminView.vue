<script lang="ts" setup>
import {ref, onMounted} from 'vue';
import {BASE_PATH, useAuthStore} from '@/stores/auth';
import {Button} from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {Badge} from '@/components/ui/badge';
import {DownloadIcon} from 'lucide-vue-next';
import {toast} from 'vue-sonner';
import {
  Table,
  TableBody,
  TableCaption, TableCell,
  TableHead,
  TableHeader,
  TableRow
} from "@/components/ui/table";
import {BarChart} from "@/components/ui/chart-bar";
import NavBar from "@/components/NavBar.vue";

const data = [
  {
    name: 'Jan',
    total: Math.floor(Math.random() * 2000) + 500,
    predicted: Math.floor(Math.random() * 2000) + 500,
  },
  {
    name: 'Feb',
    total: Math.floor(Math.random() * 2000) + 500,
    predicted: Math.floor(Math.random() * 2000) + 500,
  },
  {
    name: 'Mar',
    total: Math.floor(Math.random() * 2000) + 500,
    predicted: Math.floor(Math.random() * 2000) + 500,
  },
  {
    name: 'Apr',
    total: Math.floor(Math.random() * 2000) + 500,
    predicted: Math.floor(Math.random() * 2000) + 500,
  },
  {
    name: 'May',
    total: Math.floor(Math.random() * 2000) + 500,
    predicted: Math.floor(Math.random() * 2000) + 500,
  },
  {
    name: 'Jun',
    total: Math.floor(Math.random() * 2000) + 500,
    predicted: Math.floor(Math.random() * 2000) + 500,
  },
]

function valueFormatter(tick: number | Date) {
  return typeof tick === 'number'
    ? `$ ${new Intl.NumberFormat('us').format(tick).toString()}`
    : ''
}

const authStore = useAuthStore();
const isDownloading = ref(false);
const downloadError = ref<string | null>(null);
const users = ref([
  {
    id: '1',
    name: 'Alice Wonderland',
    email: 'alice@example.com',
    role: 'Editor',
    createdAt: '2024-01-15'
  },
  {
    id: '2',
    name: 'Bob The Builder',
    email: 'bob@example.com',
    role: 'Editor',
    createdAt: '2024-02-20'
  },
  {
    id: '3',
    name: 'Charlie Chaplin',
    email: 'charlie@example.com',
    role: 'Viewer',
    createdAt: '2024-03-10'
  },
  {
    id: '4',
    name: 'Diana Prince',
    email: 'admin@example.com',
    role: 'Admin',
    createdAt: '2024-04-01'
  },
]);
const systemInfo = ref({
  version: '1.0.0',
  uptime: '2 days 14 hours',
  memoryUsage: '65%',
});
const userStats = ref({
  totalUsers: users.value.length,
  adminUsers: users.value.filter(user => user.role === 'Admin').length,
  editorUsers: users.value.filter(user => user.role === 'Editor').length,
  viewerUsers: users.value.filter(user => user.role === 'Viewer').length,
});

const downloadBackup = async () => {
  isDownloading.value = true;
  downloadError.value = null;

  try {
    const backupUrl = BASE_PATH + '/backups/backup.zip';
    const response = await fetch(backupUrl, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      downloadError.value = errorData?.detail || `Download failed with status: ${response.status}`;
      console.error('Download failed:', downloadError.value);
      toast.error('Backup Failed', { description: downloadError.value ?? "" });
      return;
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'backup.zip';
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);

    toast.success('Backup Download Started', {
      description: 'Your backup download has started.',
    });

  } catch (error: any) {
    downloadError.value = error.message || 'An unexpected error occurred during download.';
    console.error('Download error:', downloadError.value);
    toast.error('Backup Error', { description: downloadError.value ?? ""});
  } finally {
    isDownloading.value = false;
  }
};


const updateUserStats = () => {
  userStats.value.totalUsers = users.value.length;
  userStats.value.adminUsers = users.value.filter(user => user.role === 'Admin').length;
  userStats.value.editorUsers = users.value.filter(user => user.role === 'Editor').length;
  userStats.value.viewerUsers = users.value.filter(user => user.role === 'Viewer').length;
};

onMounted(() => {
  updateUserStats();
  toast.success("FLAG{admin_panel_unlocked}",{duration:10000})
});
</script>

<template>
  <NavBar />
  <div class=" py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-3xl font-semibold text-gray-800 mb-6">Admin Dashboard</h1>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
        <Card>
          <CardHeader>
            <CardTitle>System Information</CardTitle>
            <CardDescription>Overview of the system status</CardDescription>
          </CardHeader>
          <CardContent>
            <p class="text-sm text-gray-500">Version: {{ systemInfo.version }}</p>
            <p class="text-sm text-gray-500">Uptime: {{ systemInfo.uptime }}</p>
            <p class="text-sm text-gray-500">Memory Usage: {{ systemInfo.memoryUsage }}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>User Statistics</CardTitle>
            <CardDescription>Breakdown of user roles</CardDescription>
          </CardHeader>
          <CardContent class="space-y-2">
            <p class="text-sm text-gray-500">Total Users: {{ userStats.totalUsers }}</p>
            <p class="text-sm text-gray-500">Admins: {{ userStats.adminUsers }}</p>
            <p class="text-sm text-gray-500">Editors: {{ userStats.editorUsers }}</p>
            <p class="text-sm text-gray-500">Viewers: {{ userStats.viewerUsers }}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Backup & Restore</CardTitle>
            <CardDescription>Manage application backups</CardDescription>
          </CardHeader>
          <CardContent>
            <Button
              @click="downloadBackup"
              :disabled="isDownloading"
              class="w-full"
              variant="destructive"
            >
              <DownloadIcon class="mr-2 h-4 w-4"/>
              <span v-if="isDownloading">Downloading...</span>
              <span v-else>Download Backup</span>
            </Button>
            <div v-if="downloadError" class="mt-2 text-red-500 text-sm">
              Error: {{ downloadError }}
            </div>
          </CardContent>
        </Card>
      </div>

      <div class="mb-6">
        <h2 class="text-xl font-semibold text-gray-800">Sales </h2>
        <BarChart
          :data="data"
          index="name"
          :categories="['total', 'predicted']"
          :y-formatter="(tick, i) => {
      return typeof tick === 'number'
        ? `$ ${new Intl.NumberFormat('us').format(tick).toString()}`
        : ''
    }"
        />
      </div>

      <div class="mb-6">
        <h2 class="text-xl font-semibold text-gray-800">User List</h2>
        <Table>
          <TableCaption>A list of all registered users.</TableCaption>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Role</TableHead>
              <TableHead>Created At</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="user in users" :key="user.id">
              <TableCell>{{ user.id }}</TableCell>
              <TableCell>{{ user.name }}</TableCell>
              <TableCell>{{ user.email }}</TableCell>
              <TableCell>
                <Badge v-if="user.role === 'Admin'" variant="destructive">Admin</Badge>
                <Badge v-else-if="user.role === 'Editor'" variant="secondary">Editor</Badge>
                <Badge v-else>Viewer</Badge>
              </TableCell>
              <TableCell>{{ user.createdAt }}</TableCell>
            </TableRow>
            <TableRow v-if="users.length === 0">
              <TableCell colspan="5" class="text-center">No users found.</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* Optional: Weitere spezifische Stile */
</style>
