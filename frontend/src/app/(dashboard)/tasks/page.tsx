'use client';

import { useState, useEffect } from 'react';
import { Flex, Heading, Text, Card, Button, TextField } from '@radix-ui/themes';
import { taskAPI, Task } from '@/lib/api-client';
import ProtectedRoute from '@/components/auth/protected-route';
import { authClient } from '@/lib/auth-client';

/**
 * Tasks Dashboard Page Component
 *
 * Displays all tasks for the authenticated user with CRUD functionality.
 * Protected route that redirects unauthenticated users to login.
 */
export default function TasksPage() {
  const { data: session } = authClient.useSession();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [newTask, setNewTask] = useState({ title: '', description: '' });

  useEffect(() => {
    if (session?.user?.id) {
      loadTasks();
    }
  }, [session]);

  const loadTasks = async () => {
    if (!session?.user?.id) return;

    try {
      setLoading(true);
      const userTasks = await taskAPI.getTasks(session.user.id);
      setTasks(userTasks);
    } catch (error) {
      console.error('Error loading tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newTask.title.trim() || !session?.user?.id) return;

    try {
      const createdTask = await taskAPI.createTask(session.user.id, {
        title: newTask.title,
        description: newTask.description,
      });

      setTasks([...tasks, createdTask]);
      setNewTask({ title: '', description: '' });
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  const toggleTaskCompletion = async (taskId: number) => {
    if (!session?.user?.id) return;

    try {
      const updatedTask = await taskAPI.toggleComplete(session.user.id, taskId);
      setTasks(tasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  const deleteTask = async (taskId: number) => {
    if (!session?.user?.id) return;

    try {
      await taskAPI.deleteTask(session.user.id, taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  if (!session?.user) {
    return (
      <Flex direction="column" align="center" justify="center" className="min-h-[60vh]">
        <Text>Loading...</Text>
      </Flex>
    );
  }

  return (
    <ProtectedRoute>
      <Flex direction="column" gap="6">
        {/* Page Header */}
        <Flex direction="column" gap="2">
          <Heading as="h1" size="8">
            My Tasks
          </Heading>
          <Text color="gray">
            Manage your tasks efficiently
          </Text>
        </Flex>

        {/* Add Task Form */}
        <Card>
          <Flex direction="column" gap="4">
            <Heading as="h2" size="5">
              Add New Task
            </Heading>

            <form onSubmit={handleCreateTask}>
              <Flex direction="column" gap="3">
                <TextField.Root
                  placeholder="Task title..."
                  value={newTask.title}
                  onChange={(e) => setNewTask({...newTask, title: e.target.value})}
                  required
                />
                <TextField.Root
                  placeholder="Description (optional)..."
                  value={newTask.description}
                  onChange={(e) => setNewTask({...newTask, description: e.target.value})}
                />
                <Button type="submit" className="w-fit">
                  Add Task
                </Button>
              </Flex>
            </form>
          </Flex>
        </Card>

        {/* Tasks List */}
        <Card>
          <Flex direction="column" gap="4">
            <Flex justify="between" align="center">
              <Heading as="h2" size="5">
                Your Tasks ({tasks.length})
              </Heading>
              <Text color="gray" size="2">
                {tasks.filter(t => t.completed).length} completed
              </Text>
            </Flex>

            {loading ? (
              <Text>Loading tasks...</Text>
            ) : tasks.length === 0 ? (
              <Text color="gray">No tasks yet. Add one above!</Text>
            ) : (
              <Flex direction="column" gap="3">
                {tasks.map((task) => (
                  <Flex key={task.id} justify="between" align="center" className="border-b pb-3 last:border-0 last:pb-0">
                    <Flex direction="column" gap="1">
                      <Text className={task.completed ? "line-through text-gray-500" : ""}>
                        {task.title}
                      </Text>
                      {task.description && (
                        <Text size="2" color="gray">
                          {task.description}
                        </Text>
                      )}
                      <Text size="1" color="gray">
                        Created: {new Date(task.created_at).toLocaleDateString()}
                      </Text>
                    </Flex>

                    <Flex gap="2">
                      <Button
                        variant={task.completed ? "soft" : "outline"}
                        color={task.completed ? "green" : "gray"}
                        size="1"
                        onClick={() => toggleTaskCompletion(task.id)}
                      >
                        {task.completed ? 'Completed' : 'Mark Complete'}
                      </Button>

                      <Button
                        variant="soft"
                        color="red"
                        size="1"
                        onClick={() => deleteTask(task.id)}
                      >
                        Delete
                      </Button>
                    </Flex>
                  </Flex>
                ))}
              </Flex>
            )}
          </Flex>
        </Card>
      </Flex>
    </ProtectedRoute>
  );
}