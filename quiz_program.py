import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import random
import os

class QuizProgram:
    def __init__(self, root):
        self.root = root
        self.root.title("QuizMaster v0.1")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 문제 데이터 저장소
        self.questions = []
        self.data_file = "quiz_data.json"
        self.settings_file = "quiz_settings.json"
        
        # 설정값
        self.settings = {
            "min_wrong_count": 0,
            "random_mode": True,
            "current_question_index": 0
        }
        
        # 현재 화면 관리
        self.current_frame = None
        
        # 데이터 로드
        self.load_data()
        self.load_settings()
        
        # 메인 화면 표시
        self.show_home_screen()
    
    def load_data(self):
        """JSON 파일에서 문제 데이터를 불러옵니다."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.questions = json.load(f)
            else:
                self.questions = []
        except Exception as e:
            messagebox.showerror("오류", f"데이터 로드 중 오류가 발생했습니다: {str(e)}")
            self.questions = []
    
    def load_settings(self):
        """설정 파일에서 설정값을 불러옵니다."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
        except Exception as e:
            print(f"설정 로드 중 오류: {str(e)}")
    
    def save_settings(self):
        """설정값을 JSON 파일에 저장합니다."""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("오류", f"설정 저장 중 오류가 발생했습니다: {str(e)}")
    
    def save_data(self):
        """문제 데이터를 JSON 파일에 저장합니다."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.questions, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("오류", f"데이터 저장 중 오류가 발생했습니다: {str(e)}")
    
    def clear_frame(self):
        """현재 화면을 지웁니다."""
        if self.current_frame:
            self.current_frame.destroy()
    
    def show_home_screen(self):
        """홈 화면을 표시합니다."""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 제목
        title_label = tk.Label(self.current_frame, text="퀴즈마스터 v0.1", 
                              font=("Arial", 20, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 문제 관리 프레임
        management_frame = tk.LabelFrame(self.current_frame, text="문제 관리", 
                                       font=("Arial", 12, "bold"))
        management_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 버튼 프레임
        button_frame = tk.Frame(management_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 문제 추가 버튼
        add_btn = tk.Button(button_frame, text="문제 추가", 
                           command=self.add_question, 
                           bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        add_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 문제 삭제 버튼
        delete_btn = tk.Button(button_frame, text="선택 문제 삭제", 
                              command=self.delete_question, 
                              bg="#f44336", fg="white", font=("Arial", 10, "bold"))
        delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 설정 버튼
        settings_btn = tk.Button(button_frame, text="설정", 
                                command=self.show_settings, 
                                bg="#9C27B0", fg="white", font=("Arial", 10, "bold"))
        settings_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        # 연습하기 버튼
        practice_btn = tk.Button(button_frame, text="연습하기", 
                                command=self.start_practice, 
                                bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
        practice_btn.pack(side=tk.RIGHT)
        
        # 문제 리스트 표시
        self.create_question_list(management_frame)
    
    def create_question_list(self, parent):
        """문제 리스트를 표 형식으로 표시합니다."""
        # 스크롤바가 있는 프레임
        list_frame = tk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # 트리뷰 생성
        columns = ("번호", "문제", "정답", "틀린 횟수")
        self.question_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # 더블클릭 이벤트 바인딩
        self.question_tree.bind('<Double-1>', self.edit_question)
        
        # 컬럼 설정
        self.question_tree.heading("번호", text="번호")
        self.question_tree.heading("문제", text="문제")
        self.question_tree.heading("정답", text="정답")
        self.question_tree.heading("틀린 횟수", text="틀린 횟수")
        
        self.question_tree.column("번호", width=50, anchor="center")
        self.question_tree.column("문제", width=400)
        self.question_tree.column("정답", width=150)
        self.question_tree.column("틀린 횟수", width=80, anchor="center")
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.question_tree.yview)
        self.question_tree.configure(yscrollcommand=scrollbar.set)
        
        # 배치
        self.question_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 데이터 로드
        self.refresh_question_list()
    
    def refresh_question_list(self):
        """문제 리스트를 새로고침합니다."""
        # 기존 데이터 삭제
        for item in self.question_tree.get_children():
            self.question_tree.delete(item)
        
        # 새 데이터 추가
        for i, question in enumerate(self.questions, 1):
            self.question_tree.insert("", "end", values=(
                i,
                question["question"][:50] + "..." if len(question["question"]) > 50 else question["question"],
                question["answer"],
                question["wrong_count"]
            ))
    
    def add_question(self):
        """새 문제를 추가합니다."""
        dialog = QuestionDialog(self.root, "문제 추가")
        if dialog.result:
            question_text = dialog.result["question"]
            answer_text = dialog.result["answer"]
            
            if question_text and answer_text:
                new_question = {
                    "question": question_text,
                    "answer": answer_text,
                    "wrong_count": 0
                }
                self.questions.append(new_question)
                self.save_data()
                self.refresh_question_list()
                messagebox.showinfo("성공", "문제가 추가되었습니다!")
            else:
                messagebox.showwarning("경고", "문제와 정답을 모두 입력해주세요.")
    
    def edit_question(self, event):
        """선택된 문제를 수정합니다."""
        selection = self.question_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        index = self.question_tree.index(item)
        question = self.questions[index]
        
        # 수정 다이얼로그 표시
        dialog = QuestionDialog(self.root, "문제 수정", question)
        if dialog.result:
            question_text = dialog.result["question"]
            answer_text = dialog.result["answer"]
            
            if question_text and answer_text:
                # 문제 수정
                self.questions[index]["question"] = question_text
                self.questions[index]["answer"] = answer_text
                self.save_data()
                self.refresh_question_list()
                messagebox.showinfo("성공", "문제가 수정되었습니다!")
            else:
                messagebox.showwarning("경고", "문제와 정답을 모두 입력해주세요.")
    
    def delete_question(self):
        """선택된 문제를 삭제합니다."""
        selection = self.question_tree.selection()
        if not selection:
            messagebox.showwarning("경고", "삭제할 문제를 선택해주세요.")
            return
        
        if messagebox.askyesno("확인", "선택한 문제를 삭제하시겠습니까?"):
            item = selection[0]
            index = self.question_tree.index(item)
            del self.questions[index]
            self.save_data()
            self.refresh_question_list()
            messagebox.showinfo("성공", "문제가 삭제되었습니다!")
    
    def show_settings(self):
        """설정 화면을 표시합니다."""
        dialog = SettingsDialog(self.root, self.settings, self.save_settings)
        # 설정이 저장되었으면 연습 시작
        if dialog.result:
            # 설정을 메인 클래스에 반영
            self.settings.update(dialog.settings)
            self.start_practice()
    
    def start_practice(self):
        """연습 화면을 시작합니다."""
        if not self.questions:
            messagebox.showwarning("경고", "문제가 없습니다. 먼저 문제를 추가해주세요.")
            return
        
        # 필터링된 문제 목록 생성
        filtered_questions = [q for q in self.questions if q["wrong_count"] >= self.settings["min_wrong_count"]]
        
        if not filtered_questions:
            messagebox.showwarning("경고", f"틀린 횟수가 {self.settings['min_wrong_count']}회 이상인 문제가 없습니다.")
            return
        
        self.show_practice_screen(filtered_questions)
    
    def show_practice_screen(self, practice_questions=None):
        """연습 화면을 표시합니다."""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 연습할 문제 목록 설정
        if practice_questions is None:
            self.practice_questions = self.questions
        else:
            self.practice_questions = practice_questions
        
        # 연습 세션 초기화
        self.used_questions = []  # 이미 출제된 문제들
        self.wrong_count_session = 0  # 이번 세션에서 틀린 문제 수
        self.total_questions = len(self.practice_questions)  # 총 문제 수
        
        # 순차 모드일 때 인덱스 초기화
        if not self.settings["random_mode"]:
            self.settings["current_question_index"] = 0
        
        # 제목
        title_label = tk.Label(self.current_frame, text="연습하기", 
                              font=("Arial", 20, "bold"))
        title_label.pack(pady=(0, 10))
        
        # 설정 정보 표시
        mode_text = "랜덤" if self.settings["random_mode"] else "순차"
        filter_text = f"틀린 횟수 ≥ {self.settings['min_wrong_count']}회"
        info_text = f"출제 방식: {mode_text} | 필터: {filter_text} | 문제 수: {len(self.practice_questions)}개"
        info_label = tk.Label(self.current_frame, text=info_text, 
                             font=("Arial", 10), fg="gray")
        info_label.pack(pady=(0, 10))
        
        # 진행 상황 표시
        self.progress_label = tk.Label(self.current_frame, text="", 
                                      font=("Arial", 10), fg="blue")
        self.progress_label.pack(pady=(0, 20))
        
        # 문제 표시 프레임
        question_frame = tk.LabelFrame(self.current_frame, text="문제", 
                                      font=("Arial", 12, "bold"))
        question_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.question_label = tk.Label(question_frame, text="", 
                                      font=("Arial", 14), wraplength=700, justify="left")
        self.question_label.pack(padx=10, pady=10)
        
        # 답안 입력 프레임
        answer_frame = tk.LabelFrame(self.current_frame, text="답안 입력", 
                                    font=("Arial", 12, "bold"))
        answer_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.answer_entry = tk.Entry(answer_frame, font=("Arial", 12))
        self.answer_entry.pack(fill=tk.X, padx=10, pady=10)
        self.answer_entry.bind('<Return>', self.on_enter_key)
        
        # 결과 표시
        self.result_label = tk.Label(self.current_frame, text="", 
                                    font=("Arial", 14, "bold"))
        self.result_label.pack(pady=10)
        
        # 버튼 프레임
        button_frame = tk.Frame(self.current_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # 제출 버튼
        self.submit_btn = tk.Button(button_frame, text="제출", 
                                   command=self.check_answer, 
                                   bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.submit_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 다음 문제 버튼
        self.next_btn = tk.Button(button_frame, text="다음 문제", 
                                 command=self.next_question, 
                                 bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                                 state="disabled")
        self.next_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 홈으로 버튼
        home_btn = tk.Button(button_frame, text="홈으로", 
                            command=self.show_home_screen, 
                            bg="#FF9800", fg="white", font=("Arial", 10, "bold"))
        home_btn.pack(side=tk.RIGHT)
        
        # 첫 번째 문제 표시
        self.next_question()
    
    def next_question(self):
        """다음 문제를 표시합니다."""
        if not hasattr(self, 'practice_questions') or not self.practice_questions:
            return
        
        # 아직 출제되지 않은 문제들만 필터링
        available_questions = [q for q in self.practice_questions if q not in self.used_questions]
        
        # 모든 문제를 다 풀었는지 확인
        if not available_questions:
            self.show_completion_dialog()
            return
        
        # 랜덤 모드와 순차 모드에 따라 문제 선택
        if self.settings["random_mode"]:
            self.current_question = random.choice(available_questions)
        else:
            # 순차 모드 - 아직 출제되지 않은 문제 중에서 순서대로
            remaining_indices = [i for i, q in enumerate(self.practice_questions) if q not in self.used_questions]
            if remaining_indices:
                next_index = min(remaining_indices)
                self.current_question = self.practice_questions[next_index]
        
        # 출제된 문제 목록에 추가
        self.used_questions.append(self.current_question)
        
        # 진행 상황 업데이트
        progress_text = f"진행: {len(self.used_questions)}/{self.total_questions} (틀린 문제: {self.wrong_count_session}개)"
        self.progress_label.config(text=progress_text)
        
        self.question_label.config(text=self.current_question["question"])
        self.answer_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.answer_entry.focus()
        
        # 버튼 상태 초기화
        self.submit_btn.config(state="normal")
        self.next_btn.config(state="disabled")
        
        # 답안 확인 상태 초기화 (버그 수정)
        self.answer_checked = False
    
    def on_enter_key(self, event):
        """엔터 키 이벤트 핸들러"""
        if self.submit_btn['state'] == 'normal':
            # 제출 버튼이 활성화되어 있으면 답안 확인
            self.check_answer()
        elif self.next_btn['state'] == 'normal':
            # 다음 문제 버튼이 활성화되어 있으면 다음 문제로
            self.next_question()
    
    def check_answer(self):
        """답안을 확인합니다."""
        if not hasattr(self, 'current_question'):
            return
        
        # 이미 답안을 확인한 상태라면 무시 (버그 수정)
        if hasattr(self, 'answer_checked') and self.answer_checked:
            return
        
        user_answer = self.answer_entry.get().strip()
        correct_answer = self.current_question["answer"].strip()
        
        if user_answer.lower() == correct_answer.lower():
            self.result_label.config(text="✅ 정답입니다!", fg="green")
            # 답안 확인 상태로 설정 (버그 수정)
            self.answer_checked = True
            # 정답일 때는 자동으로 다음 문제로
            self.root.after(1000, self.next_question)
        else:
            # 틀렸을 때는 정답을 보여주고 멈춤
            self.result_label.config(text=f"❌ 틀렸습니다!\n정답: {correct_answer}", fg="red")
            # 틀린 횟수 증가
            self.current_question["wrong_count"] += 1
            self.wrong_count_session += 1
            self.save_data()
            
            # 답안 확인 상태로 설정 (버그 수정)
            self.answer_checked = True
            # 다음 문제 버튼 활성화
            self.next_btn.config(state="normal")
            self.submit_btn.config(state="disabled")
    
    def show_completion_dialog(self):
        """모든 문제 완료 시 결과를 표시합니다."""
        correct_count = self.total_questions - self.wrong_count_session
        accuracy = (correct_count / self.total_questions) * 100 if self.total_questions > 0 else 0
        
        result_message = f"""모든 퀴즈를 풀었습니다!

📊 결과 요약:
• 총 문제 수: {self.total_questions}개
• 정답: {correct_count}개
• 오답: {self.wrong_count_session}개
• 정답률: {accuracy:.1f}%

{'🎉 완벽합니다!' if self.wrong_count_session == 0 else '👍 잘했습니다!' if accuracy >= 80 else '💪 더 연습해보세요!'}"""
        
        messagebox.showinfo("퀴즈 완료", result_message)
        
        # 홈 화면으로 돌아가기
        self.show_home_screen()


class SettingsDialog:
    def __init__(self, parent, settings, save_callback):
        self.settings = settings.copy()
        self.save_callback = save_callback
        self.result = False
        
        # 다이얼로그 창 생성
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("설정")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 중앙 정렬
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 100, parent.winfo_rooty() + 100))
        
        # 제목
        title_label = tk.Label(self.dialog, text="퀴즈 설정", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=(10, 20))
        
        # 틀린 횟수 필터링 설정
        filter_frame = tk.LabelFrame(self.dialog, text="문제 필터링", 
                                    font=("Arial", 12, "bold"))
        filter_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        tk.Label(filter_frame, text="오답 횟수 ≥", font=("Arial", 10)).pack(side=tk.LEFT, padx=10, pady=10)
        
        self.wrong_count_var = tk.StringVar(value=str(self.settings["min_wrong_count"]))
        wrong_count_entry = tk.Entry(filter_frame, textvariable=self.wrong_count_var, 
                                    font=("Arial", 10), width=10)
        wrong_count_entry.pack(side=tk.LEFT, padx=(0, 10), pady=10)
        
        tk.Label(filter_frame, text="만 출제", font=("Arial", 10)).pack(side=tk.LEFT, pady=10)
        
        # 출제 방식 설정
        mode_frame = tk.LabelFrame(self.dialog, text="출제 방식", 
                                  font=("Arial", 12, "bold"))
        mode_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.random_mode_var = tk.BooleanVar(value=self.settings["random_mode"])
        
        random_radio = tk.Radiobutton(mode_frame, text="랜덤 출제", 
                                     variable=self.random_mode_var, value=True,
                                     font=("Arial", 10))
        random_radio.pack(anchor="w", padx=10, pady=5)
        
        sequential_radio = tk.Radiobutton(mode_frame, text="순차 출제", 
                                         variable=self.random_mode_var, value=False,
                                         font=("Arial", 10))
        sequential_radio.pack(anchor="w", padx=10, pady=5)
        
        # 버튼 프레임
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # 연습 시작 버튼
        start_btn = tk.Button(button_frame, text="연습 시작", 
                             command=self.start_practice, 
                             bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 취소 버튼
        cancel_btn = tk.Button(button_frame, text="취소", 
                              command=self.cancel_clicked, 
                              bg="#f44336", fg="white", font=("Arial", 10, "bold"))
        cancel_btn.pack(side=tk.LEFT)
        
        # 포커스 설정
        wrong_count_entry.focus()
        
        # 대기
        self.dialog.wait_window()
    
    def start_practice(self):
        """설정을 저장하고 연습을 시작합니다."""
        try:
            # 틀린 횟수 검증
            min_wrong_count = int(self.wrong_count_var.get())
            if min_wrong_count < 0:
                messagebox.showwarning("경고", "틀린 횟수는 0 이상이어야 합니다.")
                return
            
            # 설정 업데이트
            self.settings["min_wrong_count"] = min_wrong_count
            self.settings["random_mode"] = self.random_mode_var.get()
            self.save_callback()
            
            self.result = True
            self.dialog.destroy()
                
        except ValueError:
            messagebox.showwarning("경고", "틀린 횟수는 숫자로 입력해주세요.")
    
    def cancel_clicked(self):
        """취소 버튼 클릭"""
        self.dialog.destroy()


class QuestionDialog:
    def __init__(self, parent, title, existing_question=None):
        self.result = None
        
        # 다이얼로그 창 생성
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 중앙 정렬
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # 문제 입력
        tk.Label(self.dialog, text="문제:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.question_text = tk.Text(self.dialog, height=6, font=("Arial", 10))
        self.question_text.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 정답 입력
        tk.Label(self.dialog, text="정답:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(0, 5))
        self.answer_entry = tk.Entry(self.dialog, font=("Arial", 12))
        self.answer_entry.pack(fill=tk.X, padx=10, pady=(0, 20))
        
        # 기존 문제 데이터가 있으면 미리 채워넣기
        if existing_question:
            self.question_text.insert("1.0", existing_question["question"])
            self.answer_entry.insert(0, existing_question["answer"])
        
        # 버튼 프레임
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 확인 버튼
        ok_btn = tk.Button(button_frame, text="확인", command=self.ok_clicked, 
                          bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        ok_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 취소 버튼
        cancel_btn = tk.Button(button_frame, text="취소", command=self.cancel_clicked, 
                              bg="#f44336", fg="white", font=("Arial", 10, "bold"))
        cancel_btn.pack(side=tk.RIGHT)
        
        # 포커스 설정
        self.question_text.focus()
        
        # 대기
        self.dialog.wait_window()
    
    def ok_clicked(self):
        """확인 버튼 클릭"""
        question = self.question_text.get("1.0", tk.END).strip()
        answer = self.answer_entry.get().strip()
        
        if question and answer:
            self.result = {"question": question, "answer": answer}
            self.dialog.destroy()
        else:
            messagebox.showwarning("경고", "문제와 정답을 모두 입력해주세요.")
    
    def cancel_clicked(self):
        """취소 버튼 클릭"""
        self.dialog.destroy()


def main():
    root = tk.Tk()
    app = QuizProgram(root)
    root.mainloop()


if __name__ == "__main__":
    main()