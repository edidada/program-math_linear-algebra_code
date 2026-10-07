# program-math_linear-algebra_code

《程序员的数学 3：线性代数》配套示例的多语言移植。

## Python 分支

该分支将 Ruby 示例移植为纯 Python，并用 Poetry 管理开发环境：

```powershell
poetry install
poetry run pytest
poetry run python mymatrix.py
poetry run python mat_anim.py --frame 20 | gnuplot
```

`mymatrix.py` 保留了教材演示用的显式循环、原地 LU/带选主元 LU 分解、行列式、线性方程组与求逆算法；索引仍从 1 开始，以便与原书对应。

---


#### 代码来源

> http://www.ituring.com.cn/book/1239/

---

end
