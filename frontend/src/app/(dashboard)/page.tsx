'use client';

import { useState, useEffect } from 'react';
import { Flex, Heading, Text, Card, Grid, Box } from '@radix-ui/themes';
import { taskAPI, Task } from '@/lib/api-client';
import { authClient } from '@/lib/auth-client';

/**
 * Dashboard Page Component
 *
 * Main dashboard page that displays user's task statistics and provides
 * quick access to task management features. Shows personalized welcome
 * message and task overview.
 */
export default function DashboardPage() {
  const { data: session } = authClient.useSession();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    total: 0,
    completed: 0,
    pending: 0
  });

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

      // Calculate stats
      const completed = userTasks.filter(task => task.completed).length;
      const pending = userTasks.filter(task => !task.completed).length;

      setStats({
        total: userTasks.length,
        completed,
        pending
      });
    } catch (error) {
      console.error('Error loading tasks:', error);
    } finally {
      setLoading(false);
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
    <Flex direction="column" gap="6">
      {/* Welcome Section */}
      <Flex direction="column" gap="2">
        <Heading as="h1" size="8">
          Welcome back, {session.user.name || session.user.email.split('@')[0]}!
        </Heading>
        <Text color="gray">
          Here's what's happening with your tasks today.
        </Text>
      </Flex>

      {/* Stats Cards */}
      <Grid columns={{ initial: "1", sm: "3" }} gap="4" width="100%">
        <Card>
          <Flex direction="column">
            <Text as="div" color="gray" size="2">
              Total Tasks
            </Text>
            <Heading as="h3" size="6">
              {stats.total}
            </Heading>
          </Flex>
        </Card>

        <Card>
          <Flex direction="column">
            <Text as="div" color="gray" size="2">
              Completed
            </Text>
            <Heading as="h3" size="6">
              {stats.completed}
            </Heading>
          </Flex>
        </Card>

        <Card>
          <Flex direction="column">
            <Text as="div" color="gray" size="2">
              Pending
            </Text>
            <Heading as="h3" size="6">
              {stats.pending}
            </Heading>
          </Flex>
        </Card>
      </Grid>

      {/* Quick Actions */}
      <Card>
        <Flex direction="column" gap="4">
          <Heading as="h2" size="5">
            Quick Actions
          </Heading>

          <Flex gap="3">
            <a href="/dashboard/tasks/new" className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
              Create New Task
            </a>

            <a href="/dashboard/tasks" className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
              View All Tasks
            </a>
          </Flex>
        </Flex>
      </Card>

      {/* Recent Tasks Preview */}
      {tasks.length > 0 && (
        <Card>
          <Flex direction="column" gap="3">
            <Heading as="h2" size="5">
              Recent Tasks
            </Heading>

            <Box>
              {tasks.slice(0, 5).map((task) => (
                <Flex key={task.id} justify="between" align="center" className="py-2 border-b">
                  <Text className={task.completed ? "line-through text-gray-500" : ""}>
                    {task.title}
                  </Text>
                  <Text size="2" color={task.completed ? "green" : "gray"}>
                    {task.completed ? "Completed" : "Pending"}
                  </Text>
                </Flex>
              ))}
            </Box>
          </Flex>
        </Card>
      )}
    </Flex>
  );
}