from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    keyword: str
    source_url: str
    note: str
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def summary(self) -> str:
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        return f"[{self.created_at}] {self.keyword} | 来源: {self.source_url} | 标签: {tag_str}"

    def full_text(self) -> str:
        lines = [
            f"关键词: {self.keyword}",
            f"来源: {self.source_url}",
            f"时间: {self.created_at}",
            f"标签: {', '.join(self.tags) if self.tags else '无'}",
            f"笔记: {self.note}",
        ]
        return "\n".join(lines)


@dataclass
class NoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def format_all_summaries(self) -> str:
        if not self.notes:
            return "暂无笔记。"
        return "\n\n".join(note.summary() for note in self.notes)

    def format_all_full(self) -> str:
        if not self.notes:
            return "暂无笔记。"
        separator = "\n" + "-" * 40 + "\n"
        return separator.join(note.full_text() for note in self.notes)


def demo_usage():
    collection = NoteCollection()

    note1 = KeywordNote(
        keyword="捕鱼达人",
        source_url="https://cn-fishingjoy.com",
        note="这是一款经典的海底捕鱼游戏，玩家通过瞄准和发射炮弹来捕捉不同种类的鱼，获得积分奖励。",
        tags=["游戏", "休闲", "街机"],
    )

    note2 = KeywordNote(
        keyword="捕鱼达人攻略",
        source_url="https://cn-fishingjoy.com/guide",
        note="攻略要点：优先射击大鱼，合理使用道具，注意炮弹消耗与收益平衡。",
        tags=["游戏", "攻略", "技巧"],
    )

    note3 = KeywordNote(
        keyword="渔乐无穷",
        source_url="https://cn-fishingjoy.com/community",
        note="社区用户分享的渔乐日常和捕鱼经验交流。",
        tags=["社区", "分享"],
    )

    collection.add(note1)
    collection.add(note2)
    collection.add(note3)

    print("=== 所有笔记摘要 ===")
    print(collection.format_all_summaries())

    print("\n\n=== 过滤关键词: 捕鱼达人 ===")
    for note in collection.filter_by_keyword("捕鱼达人"):
        print(note.full_text())
        print()

    print("=== 按标签过滤: 攻略 ===")
    for note in collection.filter_by_tag("攻略"):
        print(note.summary())


if __name__ == "__main__":
    demo_usage()