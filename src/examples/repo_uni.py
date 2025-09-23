"""
UniversityRepository Example Usage
Demonstrates comprehensive usage of the UniversityRepository with CRUD operations
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from db.repos.university import UniversityRepository
from models.university import UniInfo, UniLocation, UniContact, EduStats, EduScore


def main():
    """Comprehensive example of UniversityRepository usage"""
    print("=== UniversityRepository Example Usage ===\n")
    
    # Initialize repository
    connection_string = os.getenv("MONGODB_CONNECTION_STRING")
    database_name = os.getenv("MONGODB_DBNAME_UNIVERSITY")
    repo = UniversityRepository(connection_string, database_name)
    
    try:
        print("1. Repository Initialization")
        print("-" * 40)
        print(f"✓ Connected to database: {database_name}")
        print(f"✓ Connection string: {connection_string}")
        print("✓ Collection and indexes initialized")
        print()
        
        # 1. Upsert Operations (Create/Update)
        print("2. Upsert Operations (Create/Update)")
        print("-" * 40)
        
        # Create sample universities
        universities_data = [
            {
                "id": 1001,
                "name": "Massachusetts Institute of Technology",
                "overview": "MIT is a private research university in Cambridge, Massachusetts, known for its programs in engineering, science, and technology.",
                "history": "Founded in 1861, MIT has been at the forefront of technological innovation and scientific discovery.",
                "location": {
                    "address": "77 Massachusetts Ave",
                    "city": "Cambridge",
                    "state": "Massachusetts",
                    "country": "United States",
                    "postal_code": "02139"
                },
                "contact": {
                    "website": "https://web.mit.edu",
                    "phone": "+1-617-253-1000",
                    "email": "admissions@mit.edu"
                },
                "stats": {
                    "total_enrollment": 11934,
                    "undergraduate_enrollment": 4631,
                    "graduate_enrollment": 7303,
                    "international_enrollment": 3340,
                    "student_per_staff_ratio": 3.0,
                    "total_staff": 3981,
                    "faculty_count": 1000,
                    "international_ratio": 0.28,
                    "female_ratio": 0.46,
                    "male_ratio": 0.54,
                    "acceptance_rate": 0.07,
                    "graduation_rate": 0.96,
                    "retention_rate": 0.99
                },
                "score": {
                    "overall_score": 100.0,
                    "world_ranking": 1,
                    "national_ranking": 1,
                    "teaching_score": 100.0,
                    "research_score": 100.0,
                    "citation_score": 100.0,
                    "industry_score": 100.0,
                    "international_outlook_score": 100.0,
                    "reputation_score": 100.0,
                    "employer_reputation_score": 100.0,
                    "academic_reputation_score": 100.0,
                    "ranking_year": 2024
                },
                "other_info": "MIT is renowned for its cutting-edge research and innovation in fields like artificial intelligence, robotics, and biotechnology."
            },
            {
                "id": 1002,
                "name": "Stanford University",
                "overview": "Stanford University is a private research university in Stanford, California, known for its academic strength, wealth, proximity to Silicon Valley, and ranking as one of the world's top universities.",
                "history": "Founded in 1885 by Leland and Jane Stanford in memory of their only child, Leland Stanford Jr.",
                "location": {
                    "address": "450 Serra Mall",
                    "city": "Stanford",
                    "state": "California",
                    "country": "United States",
                    "postal_code": "94305"
                },
                "contact": {
                    "website": "https://www.stanford.edu",
                    "phone": "+1-650-723-2300",
                    "email": "admission@stanford.edu"
                },
                "stats": {
                    "total_enrollment": 17381,
                    "undergraduate_enrollment": 7081,
                    "graduate_enrollment": 10300,
                    "international_enrollment": 3475,
                    "student_per_staff_ratio": 4.0,
                    "total_staff": 4345,
                    "faculty_count": 2100,
                    "international_ratio": 0.20,
                    "female_ratio": 0.50,
                    "male_ratio": 0.50,
                    "acceptance_rate": 0.04,
                    "graduation_rate": 0.95,
                    "retention_rate": 0.98
                },
                "score": {
                    "overall_score": 98.4,
                    "world_ranking": 2,
                    "national_ranking": 2,
                    "teaching_score": 98.0,
                    "research_score": 99.0,
                    "citation_score": 99.0,
                    "industry_score": 98.0,
                    "international_outlook_score": 97.0,
                    "reputation_score": 99.0,
                    "employer_reputation_score": 99.0,
                    "academic_reputation_score": 99.0,
                    "ranking_year": 2024
                },
                "other_info": "Stanford is particularly known for its programs in computer science, engineering, business, and medicine."
            },
            {
                "id": 1003,
                "name": "University of Oxford",
                "overview": "The University of Oxford is a collegiate research university in Oxford, England. It is the oldest university in the English-speaking world and the world's second-oldest university in continuous operation.",
                "history": "Founded in 1096, Oxford has been a center of learning for over 900 years.",
                "location": {
                    "address": "Wellington Square",
                    "city": "Oxford",
                    "state": "Oxfordshire",
                    "country": "United Kingdom",
                    "postal_code": "OX1 2JD"
                },
                "contact": {
                    "website": "https://www.ox.ac.uk",
                    "phone": "+44-1865-270000",
                    "email": "admissions@ox.ac.uk"
                },
                "stats": {
                    "total_enrollment": 24000,
                    "undergraduate_enrollment": 12000,
                    "graduate_enrollment": 12000,
                    "international_enrollment": 12000,
                    "student_per_staff_ratio": 10.7,
                    "total_staff": 2243,
                    "faculty_count": 1200,
                    "international_ratio": 0.50,
                    "female_ratio": 0.48,
                    "male_ratio": 0.52,
                    "acceptance_rate": 0.17,
                    "graduation_rate": 0.99,
                    "retention_rate": 0.99
                },
                "score": {
                    "overall_score": 96.4,
                    "world_ranking": 3,
                    "national_ranking": 1,
                    "teaching_score": 95.0,
                    "research_score": 98.0,
                    "citation_score": 98.0,
                    "industry_score": 95.0,
                    "international_outlook_score": 99.0,
                    "reputation_score": 98.0,
                    "employer_reputation_score": 97.0,
                    "academic_reputation_score": 99.0,
                    "ranking_year": 2024
                },
                "other_info": "Oxford is known for its tutorial system, where students receive personalized instruction in small groups."
            }
        ]
        
        # Create UniInfo objects and upsert them
        for uni_data in universities_data:
            university = UniInfo(**uni_data)
            university_id = repo.upsert(university)
            print(f"✓ Upserted university: {university.name} (ID: {university_id})")
        
        print()
        
        # 2. Read Operations
        print("3. Read Operations")
        print("-" * 40)
        
        # Get university by ID
        print("Getting university by ID...")
        mit = repo.get_by_id(1001)
        if mit:
            print(f"✓ Found university by ID: {mit.name}")
            print(f"  - Country: {mit.location.country}")
            print(f"  - World Ranking: {mit.score.world_ranking}")
            print(f"  - Acceptance Rate: {mit.stats.acceptance_rate:.1%}")
        else:
            print("✗ University not found by ID")
        
        print()
        
        # Get university by name
        print("Getting university by name...")
        stanford = repo.get_by_name("Stanford University")
        if stanford:
            print(f"✓ Found university by name: {stanford.name}")
            print(f"  - Location: {stanford.location.city}, {stanford.location.state}")
            print(f"  - Total Enrollment: {stanford.stats.total_enrollment:,}")
            print(f"  - Overall Score: {stanford.score.overall_score}")
        else:
            print("✗ University not found by name")
        
        print()
        
        # Get all universities
        print("Getting all universities...")
        all_universities = repo.get_all()
        print(f"✓ Retrieved {len(all_universities)} universities:")
        for uni in all_universities:
            print(f"  - {uni.name} (ID: {uni.id}) - {uni.location.country}")
        
        print()
        
        # 3. Update Operations
        print("4. Update Operations")
        print("-" * 40)
        
        # Update Oxford's information
        print("Updating Oxford University information...")
        oxford = repo.get_by_id(1003)
        if oxford:
            # Update some statistics
            oxford.stats.total_enrollment = 25000
            oxford.score.overall_score = 96.8
            oxford.other_info = "Updated: Oxford continues to be a leading global university with strong research output and international reputation."
            
            updated_id = repo.upsert(oxford)
            print(f"✓ Updated university: {oxford.name} (ID: {updated_id})")
            print(f"  - New enrollment: {oxford.stats.total_enrollment:,}")
            print(f"  - New overall score: {oxford.score.overall_score}")
        else:
            print("✗ University not found for update")
        
        print()
        
        # 4. Search and Filter Examples
        print("5. Search and Filter Examples")
        print("-" * 40)
        
        # Find universities in the United States
        print("Finding universities in the United States...")
        us_universities = [uni for uni in all_universities if uni.location.country == "United States"]
        print(f"✓ Found {len(us_universities)} universities in the US:")
        for uni in us_universities:
            print(f"  - {uni.name} in {uni.location.city}, {uni.location.state}")
        
        print()
        
        # Find universities with high acceptance rates (more selective)
        print("Finding universities with low acceptance rates (highly selective)...")
        selective_universities = [uni for uni in all_universities if uni.stats.acceptance_rate and uni.stats.acceptance_rate < 0.10]
        print(f"✓ Found {len(selective_universities)} highly selective universities:")
        for uni in selective_universities:
            print(f"  - {uni.name}: {uni.stats.acceptance_rate:.1%} acceptance rate")
        
        print()
        
        # Find universities with high international student ratios
        print("Finding universities with high international student ratios...")
        international_universities = [uni for uni in all_universities if uni.stats.international_ratio and uni.stats.international_ratio > 0.25]
        print(f"✓ Found {len(international_universities)} universities with high international diversity:")
        for uni in international_universities:
            print(f"  - {uni.name}: {uni.stats.international_ratio:.1%} international students")
        
        print()
        
        # 5. Error Handling
        print("6. Error Handling")
        print("-" * 40)
        
        # Try to get non-existent university
        print("Trying to get non-existent university...")
        non_existent = repo.get_by_id(9999)
        if non_existent is None:
            print("✓ Correctly returned None for non-existent university")
        else:
            print("✗ Unexpected result for non-existent university")
        
        # Try to get by non-existent name
        print("Trying to get university by non-existent name...")
        non_existent_name = repo.get_by_name("Non-Existent University")
        if non_existent_name is None:
            print("✓ Correctly returned None for non-existent university name")
        else:
            print("✗ Unexpected result for non-existent university name")
        
        print()
        
        # 6. Data Analysis Examples
        print("7. Data Analysis Examples")
        print("-" * 40)
        
        # Calculate average scores by country
        print("Calculating average scores by country...")
        country_scores = {}
        for uni in all_universities:
            country = uni.location.country
            if country not in country_scores:
                country_scores[country] = []
            if uni.score.overall_score:
                country_scores[country].append(uni.score.overall_score)
        
        print("Average overall scores by country:")
        for country, scores in country_scores.items():
            if scores:
                avg_score = sum(scores) / len(scores)
                print(f"  - {country}: {avg_score:.1f} (from {len(scores)} universities)")
        
        print()
        
        # Find top-ranked universities
        print("Top-ranked universities by overall score:")
        ranked_universities = sorted(all_universities, key=lambda x: x.score.overall_score or 0, reverse=True)
        for i, uni in enumerate(ranked_universities[:3], 1):
            print(f"  {i}. {uni.name}: {uni.score.overall_score}")
        
        print()
        
        # 7. Cleanup Operations
        print("8. Cleanup Operations")
        print("-" * 40)
        
        # Remove a university
        print("Removing Stanford University...")
        success = repo.remove(1002)
        if success:
            print("✓ Successfully removed Stanford University")
        else:
            print("✗ Failed to remove Stanford University")
        
        # Verify removal
        print("Verifying removal...")
        stanford_after = repo.get_by_id(1002)
        if stanford_after is None:
            print("✓ Confirmed: Stanford University no longer exists in database")
        else:
            print("✗ Error: Stanford University still exists after removal")
        
        print()
        
        # Final count
        print("Final university count...")
        final_universities = repo.get_all()
        print(f"✓ Final count: {len(final_universities)} universities remaining")
        for uni in final_universities:
            print(f"  - {uni.name} (ID: {uni.id})")
        
        print()
        print("=== UniversityRepository Example Completed Successfully ===")
        
    except Exception as e:
        print(f"✗ Error during example execution: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Close repository connection
        print("\nClosing repository connection...")
        repo.close()
        print("✓ Repository connection closed")


if __name__ == "__main__":
    main()
