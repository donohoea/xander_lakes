cd frontend

# 1. Build the frontend
npm run build

# 2. Move files at the build root inside a root subdirectory
mkdir -p build/root
for file in $(ls build | grep -E -v '^(index\.html|static|root)$'); do
    mv "build/$file" build/root;
done

cd ..

cd backend

# 3. Build the backend
./manage.py collectstatic --no-input

cd ..
