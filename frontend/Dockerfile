FROM node:20-alpine

# Install pnpm
RUN npm install -g pnpm@10.17.1

WORKDIR /app

# Copy ALL config files first
COPY package.json pnpm-lock.yaml* jsconfig.json tailwind.config.js postcss.config.js ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy the source code
COPY . .

# Run the build
RUN pnpm run build

EXPOSE 3000

CMD ["pnpm", "start"]