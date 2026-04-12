# git init
# git branch -M main
# git remote add origin <link>
# git remote -v

git rm --cached -r .
git add .
git commit -m "${*:-unamed commit}"

git push -u origin main
